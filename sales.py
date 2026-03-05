import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

# Список сотрудников и продуктов для удобства
EMPLOYEES = [
    "Сотрудник 1",
    "Сотрудник 2",
    "Сотрудник 3",
    "Сотрудник 4",
    "Сотрудник 5"
]
PRODUCTS = ["Кредит Наличными", "Коробочное Страхование"]

class SalesApp(tk.Tk):
    """
    Основной класс приложения, который управляет окном и переключением страниц.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Конкурс Продаж")
        self.geometry("500x600")
        self.configure(bg="white")

        # Настройка шрифтов
        self.title_font = tkfont.Font(family='Arial Black', size=14)
        self.default_font = tkfont.Font(family='Arial Black', size=11)

        # Хранилище данных о продажах
        self.sales_data = {
            emp: {prod: 0 for prod in PRODUCTS} for emp in EMPLOYEES
        }

        # Контейнер для всех страниц (фреймов)
        container = tk.Frame(self, bg="white")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Создаем и сохраняем все страницы
        for F in (SelectionPage, DataEntryPage, ResultsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Показываем стартовую страницу
        self.show_frame("SelectionPage")

    def show_frame(self, page_name, employee_name=None):
        """Поднимает указанную страницу наверх."""
        frame = self.frames[page_name]
        if page_name == "DataEntryPage" and employee_name:
            frame.set_employee(employee_name)
        if page_name == "ResultsPage":
            frame.update_rankings() # Обновляем рейтинг при каждом показе
        frame.tkraise()


class SelectionPage(tk.Frame):
    """
    Страница выбора сотрудника.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label = tk.Label(
            self,
            text="Выберите сотрудника",
            font=controller.title_font,
            bg="white"
        )
        label.pack(side="top", fill="x", pady=20)

        # Создаем кнопки для каждого сотрудника
        for employee in EMPLOYEES:
            button = tk.Button(
                self,
                text=employee,
                font=controller.default_font,
                relief="solid",
                borderwidth=1,
                highlightbackground="lightgrey",
                command=lambda emp=employee: controller.show_frame(
                    "DataEntryPage", employee_name=emp
                )
            )
            # Размещаем кнопки с относительной шириной
            button.place(relx=0.15, rely=0.2 + EMPLOYEES.index(employee) * 0.1,
                         relwidth=0.7, height=40)


class DataEntryPage(tk.Frame):
    """
    Страница для ввода данных о продажах конкретного сотрудника.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.employee_name = None
        self.entries = {}
        self.operations = {}

        self.title_label = tk.Label(self, text="", font=controller.title_font, bg="white")
        self.title_label.pack(pady=20)

        # Создаем поля для ввода для каждого продукта
        for i, product in enumerate(PRODUCTS):
            frame = tk.Frame(self, bg="white")
            frame.pack(pady=10, padx=20, fill="x")

            label = tk.Label(frame, text=product, font=controller.default_font, bg="white")
            label.pack(side="left", padx=(0, 10))

            # Контейнер для полей ввода и кнопок справа
            right_container = tk.Frame(frame, bg="white")
            right_container.pack(side="right")

            entry = tk.Entry(
                right_container,
                font=controller.default_font,
                width=10,
                relief="solid",
                borderwidth=1
            )
            entry.pack(side="left")
            self.entries[product] = entry

            # Переменная для хранения выбора (+ или -)
            op_var = tk.StringVar(value="+")
            self.operations[product] = op_var

            plus_button = tk.Radiobutton(
                right_container, text="+", variable=op_var, value="+",
                bg="white", font=controller.default_font
            )
            minus_button = tk.Radiobutton(
                right_container, text="-", variable=op_var, value="-",
                bg="white", font=controller.default_font
            )
            plus_button.pack(side="left")
            minus_button.pack(side="left")

        # Кнопки управления
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=40)

        accept_button = tk.Button(
            btn_frame,
            text="Принять",
            font=controller.default_font,
            relief="solid",
            borderwidth=1,
            highlightbackground="lightgrey",
            command=self.apply_changes
        )
        accept_button.place(in_=btn_frame, relx=0.15, rely=0, relwidth=0.7, height=40)

        back_button = tk.Button(
            btn_frame,
            text="Назад",
            font=controller.default_font,
            relief="solid",
            borderwidth=1,
            highlightbackground="lightgrey",
            command=lambda: controller.show_frame("SelectionPage")
        )
        back_button.place(in_=btn_frame, relx=0.15, rely=0.2, relwidth=0.7, height=40, y=50)


    def set_employee(self, name):
        """Устанавливает имя сотрудника для этой страницы."""
        self.employee_name = name
        self.title_label.config(text=f"Показатели: {self.employee_name}")
        # Очищаем поля при выборе нового сотрудника
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def apply_changes(self):
        """Применяет введенные данные и обновляет общую статистику."""
        for product, entry in self.entries.items():
            try:
                value = int(entry.get())
            except ValueError:
                value = 0  # Если введено не число, считаем за 0

            if value > 0:
                operation = self.operations[product].get()
                if operation == "+":
                    self.controller.sales_data[self.employee_name][product] += value
                elif operation == "-":
                    self.controller.sales_data[self.employee_name][product] -= value
        
        # После применения переходим на страницу результатов
        self.controller.show_frame("ResultsPage")


class ResultsPage(tk.Frame):
    """
    Страница с итоговым рейтингом сотрудников.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label = tk.Label(self, text="Общий отчет", font=controller.title_font, bg="white")
        label.pack(pady=10)

        # Создаем вкладки
        self.notebook = ttk.Notebook(self)
        self.tab_frames = {}
        for product in PRODUCTS:
            frame = tk.Frame(self.notebook, bg="white")
            self.notebook.add(frame, text=product)
            self.tab_frames[product] = frame

        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        back_button = tk.Button(
            self,
            text="Назад к выбору сотрудника",
            font=controller.default_font,
            relief="solid",
            borderwidth=1,
            highlightbackground="lightgrey",
            command=lambda: controller.show_frame("SelectionPage")
        )
        back_button.pack(pady=15)

    def update_rankings(self):
        """Обновляет и отображает рейтинг на вкладках."""
        for product, frame in self.tab_frames.items():
            # Очищаем старые результаты
            for widget in frame.winfo_children():
                widget.destroy()

            # Собираем данные для рейтинга
            ranking_data = []
            for emp in EMPLOYEES:
                score = self.controller.sales_data[emp][product]
                ranking_data.append((emp, score))

            # Сортируем по убыванию
            ranking_data.sort(key=lambda item: item[1], reverse=True)

            # Отображаем рейтинг
            title = tk.Label(frame, text="Итоги", font=self.controller.title_font, bg="white")
            title.pack(pady=10)

            for i, (emp, score) in enumerate(ranking_data):
                rank_text = f"{i + 1}. {emp} - {score:,} руб.".replace(",", " ")
                rank_label = tk.Label(
                    frame,
                    text=rank_text,
                    font=self.controller.default_font,
                    bg="white"
                )
                rank_label.pack(anchor="w", padx=20)


if __name__ == "__main__":
    app = SalesApp()
    app.mainloop()