'''
Ваше друге завдання полягає в обчисленні значення інтеграла 
функції методом Монте-Карло.

1. Обчисліть значення інтеграла функції за допомогою методу Монте-Карло, 
інакше кажучи, знайдіть площу під цим графіком (сіра зона).

2. Перевірте правильність розрахунків, щоб підтвердити точність методу 
Монте-Карло, шляхом порівняння отриманого результату та аналітичних 
розрахунків або результату виконання функції quad. Зробіть висновки.
'''

from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi

def plot_graph(f: Callable, str_f: str, low_bound: float, high_bound: float) -> None:

    # Створення діапазону значень для x
    x = np.linspace(low_bound-0.5, high_bound+0.5, 400)
    y = f(x)

    # Створення графіка
    fig, ax = plt.subplots()

    # Малювання функції
    ax.plot(x, y, 'r', linewidth=2)

    # Заповнення області під кривою
    ix = np.linspace(low_bound, high_bound)
    iy = f(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3)

    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')

    # Додавання меж інтегрування та назви графіка
    ax.axvline(x=low_bound, color='gray', linestyle='--')
    ax.axvline(x=high_bound, color='gray', linestyle='--')
    ax.set_title(f'Графік інтегрування f(x) = {str_f} від ' + str(low_bound) + ' до ' + str(high_bound))
    plt.grid()
    

# Визначення функцій
def f1(x):
    return x**2 * np.sin(x)
def f2(x):
    return np.exp(-x**2)
def f3(x):
    return 1/(1+25*x**2)

def mc_integral_mean(f: Callable, low_bound: float, high_bound: float, n_samples: int) -> float:
    xs = np.random.uniform(low_bound, high_bound, size=n_samples)
    fx = f(xs)
    return (high_bound - low_bound) * fx.mean()

def mc_integral_hit_or_miss(f: Callable, f_max: float, low_bound: float, high_bound: float, n_samples: int) -> float:
    xs = np.random.uniform(low_bound, high_bound, size=n_samples)
    ys = np.random.uniform(0, f_max, size=n_samples)
    hits = ys <= f(xs)
    frac_hits = hits.mean()
    return frac_hits * (high_bound - low_bound) * f_max

def main():

    np.random.seed(42) 

    # кейси для тестування: опис та межі інтегрування
    test_cases = [
        {"func": f1, "str_repr": "x^2 * sin(x)", "low_bound": 0, "high_bound": 3.14, "f_max": 4},
        {"func": f2, "str_repr": "exp(-x^2)", "low_bound": 0, "high_bound": 1, "f_max": 1.2},
        {"func": f3, "str_repr": "1/(1+25*x^2)", "low_bound": 0, "high_bound": 1, "f_max": 1.2},
    ]

    n_samples = [100, 1_000, 100_000]

    for case in test_cases:
        plot_graph(case["func"], case["str_repr"], case["low_bound"], case["high_bound"])

        print("-"*50)
        print(f"Функція {case['str_repr']}")

        # Обчислення інтеграла
        result_quad, error = spi.quad(case["func"], case["low_bound"], case["high_bound"])
        print(f"Інтеграл через quad: {result_quad:.5f}, +/- {error:.9f}")


        # Обчислення методом Монте-Карло по середньому
        for n in n_samples:
            print(f"-------- {n} samples --------")
            result = mc_integral_mean(case["func"], case["low_bound"], case["high_bound"], n)
            error = result_quad - result
            print(f"Метод Монте-Карло (mean): {result:.5f} / error = {error:.5f}")


            # Обчислення методом Монте-Карло хіт-місс
            result = mc_integral_hit_or_miss(case["func"], case["f_max"], case["low_bound"], case["high_bound"], n)
            error = result_quad - result
            print(f"Метод Монте-Карло (hit-miss): {result:.5f} / error = {error:.5f}")
            
    plt.show()


if __name__ == "__main__":
    main()