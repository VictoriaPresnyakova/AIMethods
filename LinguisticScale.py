import numpy as np
import matplotlib.pyplot as plt


class LinguisticScale:
    def __init__(self, num_labels=5):
        self.num_labels = num_labels
        self.labels = {}
        self.membership_functions = {}

    def add_label(self, label, membership_func):
        self.labels[label] = membership_func
        self.save_plot_scale()

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

    def change_scale(self, label, values):

        self.add_label(label,
                       lambda x: trapezoidal_mf(x, *values) if len(values) == 4 else triangular_mf(x, *values))
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


def create_scale():
    scale = LinguisticScale()

    # Пример задания пользовательских функций принадлежности
    scale.add_label('Low', lambda x: trapezoidal_mf(x, 0, 0, 20, 40))
    scale.add_label('Medium', lambda x: triangular_mf(x, 30, 50, 70))
    scale.add_label('High', lambda x: trapezoidal_mf(x, 60, 80, 100, 100))

    return scale


if __name__ == "__main__":
    create_scale()
