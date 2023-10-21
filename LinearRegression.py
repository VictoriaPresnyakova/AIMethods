import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calc_coeff(x: list[float], y: list[float]) -> tuple:
    # len(year) * B0 + B1 * sum(price) - sum(year) = 0
    # B0 * sum(price) + B1 * sum([i * i for i in price]) - sum(year[i] * price[i] for i in range(len(year))]) = 0
    a = len(y)
    b = sum(x)
    c = sum(y)
    d = sum([i * i for i in x])
    e = sum([x[i] * y[i] for i in range(len(y))])

    b1 = (a * e - c * b) / (a * d - b * b)
    b0 = (c - b1 * b) / a
    return b0, b1


def do_predict(b0: float, b1: float, x: list[float]) -> list[float]:
    y = [b1 * i + b0 for i in x]
    return y


data = pd.read_csv(
    './data/car_price_prediction.csv',
    delimiter=',')


data = data.groupby(['Prod. year'])['Price'].agg([np.average]).reset_index()

all_prices = list(map(int, data['average']))
all_years = list(map(int, data['Prod. year']))

max_price, min_price = max(all_prices), min(all_prices)
all_prices = [(i - min_price)/(max_price - min_price) for i in all_prices]

price = all_prices[:len(all_prices) - int(len(all_prices) * 0.1)]
year = all_years[:len(all_prices) - int(len(all_years) * 0.1)]

check_price = all_prices[len(all_prices) - int(len(all_prices) * 0.1):]
check_year = all_years[len(all_years) - int(len(all_years) * 0.1):]

#print(len(all_years), len(year), len(check_year), int(len(all_years) * 0.1))

print(calc_coeff(year, price))
print(calc_coeff(check_year, check_price))

#plt.axis([0,5,0,20])
plt.title('99% data')
plt.plot(year, price, 'ro')
b0, b1 = calc_coeff(year, price)
plt.plot(year, do_predict(b0, b1, year))
plt.text(min(year), max(price), f'y={b1:.4f}*x + {b0:.4f}', fontsize=20, bbox={'facecolor':'yellow','alpha':0.2})
plt.show()


plt.title('1 % data')
plt.plot(check_year, check_price, 'ro')
b0, b1 = calc_coeff(check_year, check_price)
plt.plot(check_year, do_predict(b0, b1, check_year))
plt.text(min(check_year), max(check_price), f'y={b1:.4f}*x + {b0:.4f}', fontsize=20, bbox={'facecolor':'yellow','alpha':0.2})

plt.show()


