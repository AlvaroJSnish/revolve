# import pandas as pd
import modin.pandas as pd
import numpy as np

from common.utils import transform_values, transform_label


class Dataframe:
    label = ""
    data = np.array([])
    all_columns = np.array([])
    deleted_columns = np.array([])

    path = ""
    csv_path = ""
    dataframe = None
    dataframe_features = None
    dataframe_labels = None
    transformed_dataframe_features = None
    transformed_dataframe_labels = None

    def __init__(self, csv_path, all_columns, deleted_columns, label, path):
        self.csv_path = csv_path
        self.all_columns = all_columns
        self.deleted_columns = deleted_columns
        self.label = label
        self.path = path

        self.build_data()

    def build_data(self):
        dataframe = pd.read_csv(self.csv_path)

        for column in self.all_columns:
            if np.isin(column, self.deleted_columns):
                dataframe.drop(column, inplace=True, axis=1)

        self.dataframe = dataframe
        # save dataframe
        dataframe.to_csv(self.path + '/dataframe.csv', index=None)

        self.dataframe_features = dataframe.drop(self.label, axis=1)
        self.dataframe_labels = dataframe[self.label].copy()
        self.transformed_dataframe_features = transform_values(self.dataframe_features)
        self.transformed_dataframe_labels = transform_label(self.dataframe_labels)

    def get_transformed_data(self):
        return self.transformed_dataframe_features, self.transformed_dataframe_labels

    def get_data(self):
        return self.dataframe_features, self.dataframe_labels
