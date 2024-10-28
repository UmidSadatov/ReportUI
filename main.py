from tkinter import *
from tkinter import filedialog, messagebox, ttk
from reporter import *
from datetime import datetime
import os

from widgets.toplevels import *
from widgets.primary_tab import *
from widgets.secondary_tab import *



# Основное окно #####################################################################################

root = Tk()

root.title("ReporterUI")

icon = PhotoImage(file='images/ReporterUI_Logo.png')
root.iconphoto(False, icon)

root.geometry('1000x600+300+100')
root.resizable(False, False)

# Button(root, text="Test Button").pack()


# Открываем Notebook для вкладок
main_notebook = ttk.Notebook(root)

# Создаем две вкладки для первички и вторички
primary_tab = ttk.Frame(main_notebook)
secondary_tab = ttk.Frame(main_notebook)

# Добавим вкладки в main_notebook
main_notebook.add(primary_tab, text="Первичный отчет")
main_notebook.add(secondary_tab, text="Вторичный отчет")

# Упаковываем Notebook
main_notebook.pack(expand=True, fill='both')



BALANCE_BEGINNING_CHECKBUTTON_BOOL = BooleanVar()

INCOMES_CHECKBUTTON_BOOL = BooleanVar()

SOLD_NUMBER_CHECKBUTTON_BOOL = BooleanVar(value=True)

BALANCE_END_CHECKBUTTON_BOOL = BooleanVar()

MONTHS_LIST = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
]

SELECTED_MONTH_VAR = StringVar(value=MONTHS_LIST[datetime.now().month - 2])

CURRENT_YEAR = str(datetime.now().year - int(not bool(datetime.now().month - 1)))



# ПЕРВИЧНЫЙ ОТЧЕТ
pack_primary_main_frame(
    root, 
    primary_tab,
    BALANCE_BEGINNING_CHECKBUTTON_BOOL,
    INCOMES_CHECKBUTTON_BOOL,
    SOLD_NUMBER_CHECKBUTTON_BOOL,
    BALANCE_END_CHECKBUTTON_BOOL,
    MONTHS_LIST,
    SELECTED_MONTH_VAR,
    CURRENT_YEAR
)




# ВТОРИЧНЫЙ ОТЧЕТ
pack_secondary_main_frame(root, secondary_tab)


root.mainloop()


