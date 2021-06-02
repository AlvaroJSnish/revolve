import os

import joblib
import numpy as np
import xgboost
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV, RepeatedKFold


class TrialLinearModel:
    label = np.array([])
    features = np.array([])
    path = ""

    X_train = None
    X_test = None
    y_train = None
    y_test = None

    model = None

    test_size = 0.2

    folds = 3
    param_comb = 1
    random_state = 1001
    n_estimators = 1000
    n_thread = 1
    n_jobs = 4
    param_distributions = {
        'learning_rate': [0.05, 0.10, 0.15],
    }

    accuracy = None
    error = None

    def __init__(self, features, label, path):
        self.label = label
        self.features = features
        self.path = path

        self.create_sets()

    def create_sets(self):
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.label, test_size=self.test_size)
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def train_and_save(self):
        print('-- Creating strategy')
        skf = RepeatedKFold(
            n_splits=self.folds, random_state=self.random_state)

        print('-- Creating regressor')
        xgb = xgboost.XGBRegressor(
            n_estimators=self.n_estimators, nthread=self.n_thread)
        self.model = RandomizedSearchCV(xgb, param_distributions=self.param_distributions, n_iter=self.param_comb,
                                        n_jobs=self.n_jobs,
                                        cv=skf,
                                        verbose=10, random_state=self.random_state)

        try:
            print('-- Fitting regressor')
            self.model.fit(self.X_train, self.y_train)

            print('-- Saving regressor')
            if os.path.exists(self.path + '/model.joblib'):
                os.remove(self.path + '/model.joblib')

            joblib.dump(self.model.best_estimator_,
                        self.path + '/model.joblib')
        except ValueError as e:
            print('Oops, something went wrong fitting the model: ', e)

    def get_metrics(self):
        try:
            y_pred = self.model.predict(self.X_test)
            self.error = mean_squared_error(self.y_test, y_pred)
            predictions = [round(value) for value in y_pred]
            self.accuracy = accuracy_score(self.y_test, predictions)

            print("Accuracy: ", self.accuracy)
            print("Error: ", self.error)

            return self.error, self.accuracy
        except ValueError as e:
            print('Something went wrong getting metrics', e)
