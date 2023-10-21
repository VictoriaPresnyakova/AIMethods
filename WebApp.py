from flask import Flask, render_template, request, escape, session

from BloomFilter import BloomFilter
from ReadCSV import MyCSV

app = Flask(__name__)
my_CSV = MyCSV()
bloom_filter = BloomFilter(1000000, 100000)

v2 = 'age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,slp,caa,thall,output'.lower()

v7 = ('stock index; country; year; index price; log_indexprice; inflationrate; oil prices; exchange_rate; '
      'gdppercent; percapitaincome; unemploymentrate; manufacturingoutput; tradebalance; USTreasury; NASDAQ; '
      'FTSE 100; Nifty 50; Nikkei 225; HSI; SZCOMP; DAX 30; CAC 40; IEX 35; United States of America; United Kingdom; '
      'India; Japan; Hong Kong; China; Germany; France; Spain').lower()

v17 = ('Price; Levy; Manufacturer; Model; year; Category; Leather interior; Fuel type; Engine volume; Mileage; '
       'Cylinders; Gear box type; Drive wheels; Doors; Wheel; Color; Airbags').lower()

unique_titles = 'Manufacturer; Model; Category; Gear box type; Drive wheels; Doors; Wheel; Color'
values = v17.split('; ')
values.extend([j for i in unique_titles.split('; ') for j in my_CSV.data[i].unique()])

kaggles = {'https://www.kaggle.com/datasets/deepcontractor/car-price-prediction-challenge':
           list(map(lambda x: x.lower(), values)),
           'https://www.kaggle.com/datasets/pratik453609/economic-data-9-countries-19802020': v7.split('; '),
           'https://www.kaggle.com/datasets/rashikrahmanpritom/heart-attack-analysis-prediction-dataset?select=heart.csv': v2.split(',')}

for v in kaggles.values():
    for i in v:
        bloom_filter.add_to_filter(i.lower())


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


@app.route('/search4kaggle', methods=['POST'])
def search4kaggle():
    word = request.form['searchKaggle'].lower()
    print(word)
    if not bloom_filter.check_is_not_in_filter(word):  # it can be in list
        lst = [k for k, val in kaggles.items() if word in val]
        #print(lst)
        if lst:
            return render_template('viewlog.html', the_title="Links", info=lst)
    return entry_page()


if __name__ == '__main__':
    app.run(debug=True)
