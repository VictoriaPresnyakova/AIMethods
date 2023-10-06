import io
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Try_parse_int import try_parse_int


class MyCSV:
    def __init__(self):
        self.data = pd.read_csv(
            './data/car_price_prediction.csv',
            delimiter=',')

    @property
    def rows(self) -> int:
        return self.data.shape[0]

    @property
    def columns(self) -> int:
        return self.data.shape[1]

    def filtered_csv_file(self, columns_from: str, columns_to: str, rows_from: str, rows_to: str) -> dict:
        row_len, col_len = self.rows, self.columns

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

        return {'the_data': content, 'the_row_titles': row_titles, 'info': info.split('\n')}

    def statistics(self, column_to_group: str) -> dict:
        columns_to_show = 'Price'

        data = self.data.groupby([column_to_group])[columns_to_show].agg([min, max, np.average]).reset_index()

        row_titles = data.columns.tolist()
        text = 'min ' + columns_to_show + ' ' + str(
            data[row_titles[0]][data[row_titles[1]] == data[row_titles[1]].min()]
            .to_numpy()) + '\n' \
                           'max ' + columns_to_show + ' ' + str(
            data[row_titles[0]][data[row_titles[2]] == data[row_titles[2]].max()]
            .to_numpy()) + '\n' \
                           'min average' + columns_to_show + ' ' + str(
            data[row_titles[0]][data[row_titles[3]] == data[row_titles[3]].min()]
            .to_numpy()) + '\n' \
                           'max average' + columns_to_show + ' ' + str(
            data[row_titles[0]][data[row_titles[3]] == data[row_titles[3]].max()]
            .to_numpy())
        data = data.to_numpy()
        return {'the_data': data, 'the_row_titles': row_titles, 'info': text.split('\n')}

    def add_data(self, percent: int = 5):
        ad_df = {}
        for i in self.data.columns.tolist():
            arr = []
            for kol in range(int(self.rows * (percent / 100))):
                if isinstance(self.data[i][0], str):
                    arr.append(self.data[i].value_counts().reset_index().to_numpy()[0][0])
                else:
                    avg = self.data[i].mean()
                    p = 0.005 if i == 'Prod. year' else 0.1
                    avg += random.uniform(-avg * p, avg * p)
                    arr.append(int(avg) if i == 'Prod. year' or i == 'Airbags' else avg)
            ad_df[i] = arr
        df2 = pd.DataFrame(ad_df)
        self.data = pd.concat([df2, self.data], ignore_index=True)

    def diagram(self):
        column_to_group = ['Prod. year', 'Manufacturer', 'Category', 'Fuel type']
        columns_to_show = 'Price'

        for i in column_to_group:
            data = self.data.groupby([i])[columns_to_show].mean()
            plt.bar(data.index, data.values, color='blue')
            plt.title(f'{i}  {columns_to_show}')
            plt.show()

        self.add_data()

        for i in column_to_group:
            data = self.data.groupby([i])[columns_to_show].mean()
            plt.title(f'{i}  {columns_to_show} with added data')
            plt.bar(data.index, data.values, color='blue')
            plt.show()