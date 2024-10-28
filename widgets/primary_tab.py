from tkinter import *
from tkinter import ttk

from .toplevels import *



PRIMARY_INPUT_DIST_FILES = []

PRIMARY_SELECTED_DIST_FILE_INDEX = None

PRIMARY_CURRENT_RENDERED_FILE = None




# ПЕРВИЧНЫЙ ОТЧЕТ

def pack_primary_main_frame(
        root, 
        primary_tab:ttk.Frame,
        balance_beginning_checkbutton_bool:BooleanVar,
        incomes_checkbutton_bool:BooleanVar,
        sold_number_checkbutton_bool:BooleanVar,
        balance_end_checkbutton_bool:BooleanVar,
        months_list:list[str],
        selected_month_var:StringVar,
        current_year:str
    ):
    primary_main_frame = Frame(primary_tab, width=1000, height=500, background="lightgrey")
    primary_main_frame.pack_propagate(False)
    primary_main_frame.pack()

    # Слева: файлы дистрибьюторов #######################################################################
    input_frame = Frame(primary_main_frame, width=500, height=500, background="lightgrey")
    input_frame.pack_propagate(False)
    input_frame.pack(side=LEFT)

    input_frame_title = Label(input_frame, text="Файлы дистрибьютеров", background="lightgrey", font=("Arial", 10, "bold"))
    input_frame_title.pack(pady=5)

    input_listbox_frame = Frame(input_frame, width=500, height=420, background="lightgrey")
    input_listbox_frame.pack_propagate(False)
    input_listbox_frame.pack(anchor='nw')

    input_listbox_scrollbar = Scrollbar(input_listbox_frame)
    input_listbox_scrollbar.pack(side=RIGHT, fill=Y)

    input_listbox = Listbox(input_listbox_frame, width=78, yscrollcommand=input_listbox_scrollbar.set)
    input_listbox.pack(side=RIGHT, fill=Y)

    # Кнопка "Добавить" для добавления новых данных
    new_data_edit_button = Button(
        input_frame, 
        text="Добавить",
        command=lambda:open_primary_template_modal(
            root,
            input_listbox,
            open_file_button,
            render_button,
            not_found_names_listbox,
            PRIMARY_SELECTED_DIST_FILE_INDEX,
            PRIMARY_CURRENT_RENDERED_FILE,
            PRIMARY_INPUT_DIST_FILES
        )
    )
    new_data_edit_button.pack(pady=10)

    # Кнопка для очистки списка файлов дистрибьюторов
    clear_input_lisbox_button = Button(input_frame, text="Очистить")
    clear_input_lisbox_button.place(x=10, y=460)


    # Справа:  #######################################################################################################

    right_frame = Frame(primary_main_frame, width=500, height=500, background="lightgrey")
    right_frame.pack_propagate(False)
    right_frame.pack()


    # Справа сверху: ненайденные наименования: #######################################################################

    not_found_names_frame = Frame(right_frame, width=500, height=250, background="lightgrey")
    not_found_names_frame.pack_propagate(False)
    not_found_names_frame.pack()

    not_found_names_frame_title = Label(not_found_names_frame, text="Ненайденные наименования", background="lightgrey", font=("Arial", 10, "bold"))
    not_found_names_frame_title.pack(pady=5)

    not_found_names_listbox_frame = Frame(not_found_names_frame, width=500, height=420, background="lightgrey")
    not_found_names_listbox_frame.pack_propagate(False)
    not_found_names_listbox_frame.pack(anchor='nw')

    not_found_names_listbox_scrollbar = Scrollbar(not_found_names_listbox_frame)
    not_found_names_listbox_scrollbar.pack(side=RIGHT, fill=Y)

    not_found_names_listbox = Listbox(not_found_names_listbox_frame, width=78, yscrollcommand=not_found_names_listbox_scrollbar.set)
    not_found_names_listbox.pack(side=RIGHT, fill=Y)


    # Справа снизу: параметры  #####################################################################################

    parameters_frame = Frame(right_frame, width=500, height=250, background="lightgrey")
    parameters_frame.pack_propagate(False)
    parameters_frame.pack()

    parameters_frame_title = Label(parameters_frame, text="Параметры", background="lightgrey", font=("Arial", 15, "bold"))
    parameters_frame_title.pack(pady=5)

    # Frame(parameters_frame, height=10, background="lightgrey").pack()

    # Указание месяца и года (для ежегодного отчета)
    # Месяц
    month_frame = Frame(parameters_frame, background="lightgrey")
    month_frame.pack(padx=150, anchor='w')

    month_label = Label(month_frame, text="Месяц:", background="lightgrey", font=("Arial", 12))
    month_label.pack(side=LEFT)

    month_dropdown = OptionMenu(month_frame, selected_month_var, *months_list)
    month_dropdown.config(width=18, font=("Arial", 12))
    month_dropdown.pack()
    
    # Год
    year_frame = Frame(parameters_frame, background="lightgrey")
    year_frame.pack(padx=150, anchor='w')

    year_label = Label(year_frame, text="Год:     ", background="lightgrey", font=("Arial", 12))
    year_label.pack(side=LEFT)

    year_entry = Entry(year_frame, width=5, font=("Arial", 12))
    year_entry.insert(0, current_year)
    year_entry.pack()



    # Параметры, которые должны быть в эксель-файле
    balance_beginning_checkbutton = Checkbutton(
        parameters_frame, 
        text="Остаток в начале", 
        variable=balance_beginning_checkbutton_bool, 
        background="lightgrey",
        font=("Arial", 12)
    )
    balance_beginning_checkbutton.pack(padx=150, anchor='w')

    incomes_checkbutton = Checkbutton(
        parameters_frame, 
        text="Приход", 
        variable=incomes_checkbutton_bool, 
        background="lightgrey",
        font=("Arial", 12)
    )
    incomes_checkbutton.pack(padx=150, anchor='w')

    sold_number_checkbutton = Checkbutton(
        parameters_frame, 
        text="Продажа", 
        background="lightgrey",
        variable=sold_number_checkbutton_bool,
        font=("Arial", 12, "bold")
    )    
    sold_number_checkbutton.pack(padx=150, anchor='w')

    balance_end_checkbutton = Checkbutton(
        parameters_frame, 
        text="Остаток в конце", 
        variable=balance_end_checkbutton_bool, 
        background="lightgrey",
        font=("Arial", 12)
    )
    balance_end_checkbutton.pack(padx=150, anchor='w')

    #  Нижняя рамка кнопок

    Frame(primary_tab, height=10).pack()

    render_button = Button(primary_tab, text="Расчитать", font=('Arial', 12, 'bold'), state="disabled")
    render_button.pack(pady=0)

    open_file_button = Button(primary_tab, text="Открыть файл", state="disabled")
    open_file_button.pack(side=RIGHT, anchor='n', padx=20)


    # модальное окно для редактирования БД:
    database_button = Button(primary_tab, text="База данных", command=lambda:open_database_modal(root))
    database_button.pack(side=LEFT, anchor='n', padx=20)


