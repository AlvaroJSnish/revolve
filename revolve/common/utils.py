import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder


def transform_label(series):
    column_type = series.dtype

    if column_type == object:
        pipeline = LabelEncoder()
        transformed_label = pipeline.fit_transform(series)
        return transformed_label

    return series


def transform_values(dataframe):
    numerical_columns = dataframe.select_dtypes(np.number).columns
    categorical_columns = dataframe.select_dtypes(exclude=[np.number]).columns

    tmp_cat_df = dataframe.copy()
    tmp_num_df = dataframe.copy()

    for column in numerical_columns:
        tmp_cat_df.drop(column, inplace=True, axis=1)

    for column in categorical_columns:
        tmp_num_df.drop(column, inplace=True, axis=1)

    num_pipeline = numerical_transformer()
    cat_pipeline = categorical_transformer()

    full_pipeline = ColumnTransformer(transformers=[
        ('num', num_pipeline, list(numerical_columns)),
        ('cat', cat_pipeline, list(categorical_columns))
    ])

    transformed_dataframe = full_pipeline.fit_transform(dataframe)

    return transformed_dataframe


def numerical_transformer():
    numerical_pipeline = Pipeline(steps=[
        ('imputer_num', SimpleImputer(strategy='median', missing_values=np.nan)),
        ('std_scaler', StandardScaler())
    ])
    return numerical_pipeline


def categorical_transformer():
    categorical_pipeline = Pipeline(steps=[
        ('imputer_cat', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    return categorical_pipeline
