from flask import Flask, render_template, request, escape, session
import numpy as np
import pandas as pd
import Try_parse_int as tr

app = Flask(__name__)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome!')


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    data = pd.read_csv(
        './data/world-population-by-country-2020.csv',
        delimiter=',')

    row_titles = data.columns.tolist()

    columns_from = tr.try_parse_int(request.form['columns_from'], 1) - 1
    columns_to = tr.try_parse_int(request.form['columns_to'], len(row_titles))

    data = data[row_titles[columns_from if columns_from >= 0 else 0:
                           columns_to if columns_from < columns_to < len(row_titles) else len(row_titles) - 1]]
    row_titles = data.columns.tolist()

    content = data.to_numpy()

    rows_from = tr.try_parse_int(request.form['rows_from'], 1) - 1
    rows_to = tr.try_parse_int(request.form['rows_to'], len(content))

    content = content[rows_from if rows_from >= 0 else 0:
                      rows_to if rows_from < rows_to < len(content) else len(content) - 1]
    return render_template('viewlog.html', the_title='View Log',
                           the_row_titles=row_titles, the_data=content)


if __name__ == '__main__':
    app.run(debug=True)
