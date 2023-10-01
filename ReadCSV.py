import io
import pandas as pd
from numpy import ndarray
from Try_parse_int import try_parse_int


def filtered_csv_file(columns_from: str, columns_to: str, rows_from: str, rows_to: str) -> tuple:
    data = pd.read_csv(
        './data/car_price_prediction.csv',
        delimiter=',')
    row_len, col_len = data.shape

    columns_from = try_parse_int(columns_from, 1) - 1
    columns_to = try_parse_int(columns_to, col_len)

    rows_from = try_parse_int(rows_from, 1) - 1
    rows_to = try_parse_int(rows_to, row_len)

    data = data.iloc[rows_from if rows_from >= 0 else 0:
                     rows_to if rows_from < rows_to < row_len else row_len,
                     columns_from if columns_from >= 0 else 0:
                     columns_to if columns_from < columns_to < col_len else col_len]

    row_titles = data.columns.tolist()

    content = data.to_numpy()

    buffer = io.StringIO()
    data.info(buf=buffer)
    info = buffer.getvalue()

    return content, row_titles, info.split('\n')
