import io

import numpy
import numpy as np
import pandas as pd
from Try_parse_int import try_parse_int


class MyCSV:
    def __init__(self):
        self.data = pd.read_csv(
            './data/car_price_prediction.csv',
            delimiter=',')

    def filtered_csv_file(self, columns_from: str, columns_to: str, rows_from: str, rows_to: str) -> tuple:
        row_len, col_len = self.data.shape

        columns_from = try_parse_int(columns_from, 1) - 1
        columns_to = try_parse_int(columns_to, col_len)

        rows_from = try_parse_int(rows_from, 1) - 1
        rows_to = try_parse_int(rows_to, row_len)

        data = self.data.iloc[rows_from if rows_from >= 0 else 0:
                              rows_to if rows_from < rows_to < row_len else row_len,
               columns_from if columns_from >= 0 else 0:
               columns_to if columns_from < columns_to < col_len else col_len]

        row_titles = data.columns.tolist()

        content = data.to_numpy()

        buffer = io.StringIO()
        data.info(buf=buffer)
        info = buffer.getvalue()

        return content, row_titles, info.split('\n')

    def statistics(self, column_to_group: str) -> tuple:
        columns_to_show = ['Price']
        first_column = sorted(self.data[column_to_group].unique())

        data = self.data.groupby([column_to_group])[columns_to_show].agg([np.min, np.max, np.average])
        row_titles = [''] + data.columns.tolist()
        data = data.to_numpy()
        new_column = np.array(first_column).reshape(-1, 1)
        result_matrix = np.hstack((new_column, data))
        return result_matrix, row_titles
