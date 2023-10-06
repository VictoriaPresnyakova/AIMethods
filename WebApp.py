from flask import Flask, render_template, request, escape, session

from ReadCSV import MyCSV

app = Flask(__name__)
my_CSV = MyCSV()


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome!')


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    kwargs = my_CSV.filtered_csv_file(request.form['columns_from'], request.form['columns_to'],
                                      request.form['rows_from'], request.form['rows_to'])
    return render_template('viewlog.html', the_title="Data", **kwargs)


@app.route('/statistics', methods=['POST'])
def do_statistics() -> 'html':
    option = request.form['option']
    kwargs = my_CSV.statistics(option)
    return render_template('viewlog.html', the_title=option, **kwargs)


@app.route('/add_rows', methods=['POST'])
def add_rows():
    my_CSV.add_data()
    return do_search()


if __name__ == '__main__':
    app.run(debug=True)
