import numbers
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


def transform_values(dataframe):
    types = dataframe.columns.to_series().groupby(dataframe.dtypes).groups
    numerical_columns = dataframe.select_dtypes(np.number).columns
    categorical_columns = dataframe.select_dtypes(exclude=[np.number]).columns

    num_pipeline = fill_num_values(dataframe, categorical_columns)
    # cat_pipeline = fill_cat_values(dataframe, numerical_columns)

    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, list(numerical_columns)),
        # ("cat", cat_pipeline, list(categorical_columns))
    ])

    encoder = LabelEncoder()
    df = dataframe[categorical_columns].apply(encoder.fit_transform)
    dataframe = dataframe.assign(**df.to_dict())

    dataframe_transformed = full_pipeline.fit_transform(dataframe)

    return dataframe, dataframe_transformed


def fill_num_values(dataframe, categorical_columns):
    df_copy = dataframe.copy()

    for column in categorical_columns:
        df_copy.drop(column, inplace=True, axis=1)

    numerical_pipeline = Pipeline([
        ('imputer_num', SimpleImputer(strategy="median")),
        ('std_scaler', StandardScaler())
    ])

    dataframe_num = numerical_pipeline.fit_transform(df_copy)

    return numerical_pipeline


# def fill_cat_values(dataframe, numerical_columns):
#     encoder = LabelEncoder()
#     df_copy = dataframe.copy()

#     for column in numerical_columns:
#         df_copy.drop(column, inplace=True, axis=1)

#     columns = df_copy.columns

#     for column in columns:
#         df_copy[column] = encoder.fit_transform(df_copy[column].astype(str))

#     return encoder