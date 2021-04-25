import numpy as np
import pandas as pd

from common.utils import transform_values, transform_label


class Dataframe:
    label = ""
    data = np.array([])
    all_columns = np.array([])
    deleted_columns = np.array([])

    dataframe = None
    dataframe_features = None
    dataframe_labels = None
    transformed_dataframe_features = None
    transformed_dataframe_labels = None

    def __init__(self, data, all_columns, deleted_columns, label):
        self.data = data
        self.all_columns = all_columns
        self.deleted_columns = deleted_columns
        self.label = label

        self.build_data()

    def build_data(self):
        dataframe = pd.DataFrame(
            data=self.data, columns=self.all_columns, index=None)

        for column in self.all_columns:
            if np.isin(column, self.deleted_columns):
                dataframe.drop(column, inplace=True, axis=1)

        self.dataframe = dataframe
        self.dataframe_features = dataframe.drop(self.label, axis=1)
        self.dataframe_labels = dataframe[self.label].copy()
        self.transformed_dataframe_features = transform_values(self.dataframe_features)
        self.transformed_dataframe_labels = transform_label(self.dataframe_labels)

    def get_transformed_data(self):
        return self.transformed_dataframe_features, self.transformed_dataframe_labels

    def get_data(self):
        return self.dataframe_features, self.dataframe_labels
