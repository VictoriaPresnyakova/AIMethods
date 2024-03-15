import numpy as np
import matplotlib.pyplot as plt


class LinguisticScale:
    def __init__(self):
        self.labels = {}
        # Пример задания пользовательских функций принадлежности
        self.add_label('Low', [0, 0, 20, 40])
        self.add_label('Medium', [30, 50, 70])
        self.add_label('High', [60, 80, 100, 100])

    # def add_label(self, label, membership_func):
    #     self.labels[label] = membership_func
    #     self.save_plot_scale()

    def save_plot_scale(self):
        ox = np.linspace(0, 100, 1000)
        plt.figure(figsize=(10, 6))
        for label, membership_func in self.labels.items():
            plt.plot(ox, membership_func(ox), label=label)
        plt.title('Linguistic Scale')
        plt.xlabel('Salary Level')
        plt.ylabel('Membership Degree')
        plt.legend()
        plt.grid(True)
        # plt.show()
        plt.savefig('static/images/plot.png')

    def add_label(self, label, values):
        self.labels[label] = lambda x: trapezoidal_mf(x, *values) if len(values) == 4 \
            else triangular_mf(x, *values)
        self.save_plot_scale()


def triangular_mf(x, a, b, c):
    return [help_triangular_mf(xi, a, b, c) for xi in x]


def help_triangular_mf(x, a, b, c):
    if a <= x <= b:
        return (x - a) / (b - a)
    if b < x <= c:
        return (c - x) / (c - b)
    return 0


def trapezoidal_mf(x, a, b, c, d):
    return [help_trapezoidal_mf(xi, a, b, c, d) for xi in x]


def help_trapezoidal_mf(x, a, b, c, d):
    if a <= x <= b:
        return (x - a) / (b - a)
    if b < x < c:
        return 1
    if c <= x <= d:
        return (d - x) / (d - c)
    return 0

