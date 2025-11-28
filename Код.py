#task1.py

import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AddDigitGUI:
    """Клас графічного інтерфейсу для демонстрації роботи функції AddRightDigit."""

    def __init__(self, master):
        self.master = master
        master.title("Func29 — AddRightDigit")
        master.geometry("600x500")

        # Ввід даних
        tk.Label(master, text="Початкове число K:").pack()
        self.entry_k = tk.Entry(master)
        self.entry_k.pack()

        tk.Label(master, text="Цифра D1 (0–9):").pack()
        self.entry_d1 = tk.Entry(master)
        self.entry_d1.pack()

        tk.Label(master, text="Цифра D2 (0–9):").pack()
        self.entry_d2 = tk.Entry(master)
        self.entry_d2.pack()

        # Кнопка
        tk.Button(master, text="Обчислити", command=self.calculate).pack(pady=10)

        # Поле результатів
        self.result_label = tk.Label(master, text="", font=("Arial", 12))
        self.result_label.pack()

        # Графік 
        fig = Figure(figsize=(5, 2.5))
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Метод AddRightDigit
    def AddRightDigit(self, D: int, K: int) -> int:
        """Додає цифру D праворуч до числа K."""
        return K * 10 + D

    # Основна функція обробки натискання кнопки
    def calculate(self):
        """Зчитує дані, проводить розрахунки і показує результати."""
        try:
            K = int(self.entry_k.get())
            D1 = int(self.entry_d1.get())
            D2 = int(self.entry_d2.get())

            if not (0 <= D1 <= 9 and 0 <= D2 <= 9):
                raise ValueError

        except ValueError:
            messagebox.showerror("Помилка", "Перевірте правильність введення даних!")
            return

        # Обчислення
        res1 = self.AddRightDigit(D1, K)
        res2 = self.AddRightDigit(D2, res1)

        # Відображення текстового результату
        self.result_label.config(
            text=f"Після додавання D1: {res1}\n"
                 f"Після додавання D2: {res2}"
        )

        # Побудова графіка
        self.ax.clear()
        self.ax.plot([0, 1, 2], [K, res1, res2], marker="o")
        self.ax.set_title("Результати додавання цифр")
        self.ax.set_xlabel("Крок")
        self.ax.set_ylabel("Значення")
        self.canvas.draw()



# task2.py

import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np
import os


class ScriptGUI:
    """
    Графічний інтерфейс для побудови графіка та обчислення рекурентного виразу
    Варіант 2.
    Відповідальність: забезпечує введення параметрів, обчислення, збереження і 
    візуалізацію даних.
    """

    def __init__(self, master):
        self.master = master
        master.title("lab5_328-v02-Hliebova-Karina")
        master.geometry("700x500")

        # Ввід даних
        tk.Label(master, text="Кількість точок N (20..1000):").pack()
        self.entry_N = tk.Entry(master)
        self.entry_N.pack()
        self.entry_N.insert(0, "100")  # Значення за замовчуванням

        tk.Button(master, text="Створити файл та графік", command=self.run_simulation).pack(pady=10)

    # Основні методи 
    def run_simulation(self):
        try:
            N = int(self.entry_N.get())
            if not 20 <= N <= 1000:
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка", "Введіть число N у діапазоні 20..1000!")
            return

        # Параметри
        T = 0.1
        K_param = 3
        xi = 0.2
        T0 = 2 * T / N

        # Початкові умови
        U = np.zeros(N + 2)
        y = np.zeros(N + 2)
        U[0] = 0.1
        y[0] = 0
        y[1] = 0

        # Масив часу
        t = np.array([k * T0 for k in range(N + 2)])

        # Рекурентне обчислення
        for k in range(N):
            y[k + 2] = ((2 - (2 * xi * T0) / T) * y[k + 1] +
                        ((2 * xi * T0) / T - 1 - (T0**2) / (T**2)) * y[k] +
                        ((K_param * T0**2) / (T**2)) * U[k])

        # Створення текстового файлу 
        filename = "lab5_data.txt"
        with open(filename, "w") as f:
            for i in range(N + 2):
                f.write(f"{t[i]};{y[i]}\n")  # Варіант 2 -> парний -> ';'

        # Зчитування даних
        X, Y = [], []
        with open(filename, "r") as f:
            for line in f:
                x_str, y_str = line.strip().split(";")
                X.append(float(x_str))
                Y.append(float(y_str))

        X = np.array(X)
        Y = np.array(Y)

        # Мін/макс 
        min_x, max_x = np.min(X), np.max(X)
        min_y, max_y = np.min(Y), np.max(Y)

        messagebox.showinfo("Мін/Макс значення",
                            f"Аргумент (t): min={min_x:.4f}, max={max_x:.4f}\n"
                            f"Функція (y): min={min_y:.4f}, max={max_y:.4f}")

        # Побудова графіка 
        plt.figure(figsize=(10, 5))
        plt.plot(X, Y, marker='o', markersize=3, label='Кут тангажa (υ), рад')
        plt.title("Характеристика одного з об'єктів управління: кут тангажa літака (υ)")
        plt.xlabel("Час t [с]")
        plt.ylabel("Кут тангажa y [рад]")
        plt.grid(True)
        plt.legend()
        plt.show()




#script-file

import tkinter as tk
from tkinter import messagebox
import sys

# Імпорт класів з попередніх файлів
from task1 import AddDigitGUI
from task2 import ScriptGUI  # Припустимо, файл із завдання 2 називається lab5_task2.py


def main_menu():
    while True:
        print("\n=== Головне меню ===")
        print("1: Завдання 1 — AddRightDigit GUI")
        print("2: Завдання 2 — Lab5 GUI")
        print("0: Вийти")
        choice = input("Виберіть завдання: ")

        if choice == "1":
            root1 = tk.Tk()
            app1 = AddDigitGUI(root1)
            root1.mainloop()
        elif choice == "2":
            root2 = tk.Tk()
            app2 = ScriptGUI(root2)
            root2.mainloop()
        elif choice == "0":
            print("Вихід із програми...")
            sys.exit()
        else:
            print("Невірний вибір, спробуйте ще раз.")


if __name__ == "__main__":
    main_menu()
