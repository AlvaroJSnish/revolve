import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import xgboost
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV

from celery import shared_task
from common.utils import transform_values, transform_label
from projects.models import ProjectConfiguration


@shared_task(serializer='json')
def train_regression_model(request, project_configuration_id):
    try:
        os.makedirs('uploads/' + request['file_url'])
        p_path = 'uploads/' + request['file_url']

        # get the data from the request
        data = request['final_data']
        label = request['label']
        all_columns = np.array(request['all_columns'])
        saved_columns = np.array(request['saved_columns'])
        deleted_columns = np.array(request['deleted_columns'])

        # create the dataframe
        dataframe = pd.DataFrame(
            data=data, columns=all_columns, index=None)

        # drop columns listed on deleted_columns
        for column in all_columns:
            if np.isin(column, deleted_columns):
                dataframe.drop(column, inplace=True, axis=1)

        # features and labels
        dataframe_features = dataframe.drop(label, axis=1)
        dataframe_labels = dataframe[label].copy()

        # transform the values
        transformed_dataframe_features = transform_values(dataframe_features)
        transformed_dataframe_labels = transform_label(dataframe_labels)

        test_size = 0.2
        X_train, X_test, y_train, y_test = train_test_split(
            transformed_dataframe_features, transformed_dataframe_labels, test_size=test_size)

        params = {
            'min_child_weight': [1, 3, 5, 7, 10],
            'gamma': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 5],
            'subsample': [0.6, 0.8, 1.0],
            'colsample_bytree': [0.3, 0.4, 0.6, 0.8, 1.0],
            'max_depth': [3, 4, 5, 6, 8, 10, 12, 15, 17, 19, 21],
            'learning_rate': [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
        }
        folds = 50
        param_comb = 6
        random_state = 1001
        n_estimators = 250
        n_thread = 1
        n_jobs = 4

        skf = StratifiedKFold(
            n_splits=folds, shuffle=True, random_state=random_state)

        xgb = xgboost.XGBRegressor(n_estimators=n_estimators, nthread=n_thread)
        model = RandomizedSearchCV(xgb, param_distributions=params, n_iter=param_comb, n_jobs=n_jobs,
                                   cv=skf.split(
                                       X_train, y_train), verbose=3, random_state=random_state)

        model.fit(X_train, y_train)

        joblib.dump(model.best_estimator_, p_path + '/model.joblib')

        # testing
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, predictions)

        project_configuration = ProjectConfiguration.objects.get(id=project_configuration_id)

        project_configuration.trained = True
        project_configuration.last_time_trained = datetime.now()
        project_configuration.accuracy = accuracy
        project_configuration.error = mse
        project_configuration.training_task_status = 'SUCCESS'
        project_configuration.save(force_update=True)

    except ValueError:
        project_configuration = ProjectConfiguration.objects.get(id=project_configuration_id)
        os.removedirs('uploads/' + request.data['file_url'])
        project_configuration.trained = False
        project_configuration.last_time_trained = datetime.now()
        project_configuration.training_task_status = 'REVOKED'
        project_configuration.save(force_update=True)
