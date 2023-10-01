from flask import Flask, render_template, request, escape, session
import pandas as pd
from ReadCSV import filtered_csv_file


app = Flask(__name__)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome!')


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    content, titles, info = filtered_csv_file(request.form['columns_from'], request.form['columns_to'],
                             request.form['rows_from'], request.form['rows_to'])
    return render_template('viewlog.html', the_title="Data",
                           the_data=content, the_row_titles=titles, info=info)


if __name__ == '__main__':
    app.run(debug=True)
