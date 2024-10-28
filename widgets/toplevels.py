from tkinter import *
from tkinter import filedialog, messagebox, ttk
from reporter import *
from datetime import datetime
import os


# ШАБЛОН ДЛЯ ПЕРВИЧНЫХ ФАЙЛОВ

def open_primary_template_modal(
        master,
        input_listbox,
        open_file_button,
        render_button,
        not_found_names_listbox,
        primary_selected_dist_file_index,
        primary_current_rendered_file,
        primary_input_dist_files,
        title = "Новые данные",
        file_txt = "Файл не выбран",
        distributor = "Не выбрано",
        sheet_index = "0",
        name_column = "",
        balance_beginning_column = "", 
        incomes_column = "", 
        sold_number_column = "", 
        balance_end_column = "", 
        start_row_number = "1",
        enable_delete_button = False,
        mode = "create",
):
    data_edit_modal = Toplevel(master)
    data_edit_modal.title(title)

    icon = PhotoImage(file='images/ReporterUI_Logo.png')
    data_edit_modal.iconphoto(False, icon)

    # Задание размера и позиции окна (ширинаxвысота+x+y)
    data_edit_modal.geometry("550x430+600+200")

    # Сделать окно модальным
    data_edit_modal.transient(master)  # Сделать его подчинённым к основному окну
    data_edit_modal.grab_set()  # Захватить все события до закрытия окна

    # Запретить изменение размера окна
    data_edit_modal.resizable(False, False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # УКАЗАНИЕ ФАЙЛА ############################

    file_frame = Frame(data_edit_modal)
    file_frame.pack(pady=5, anchor='w', padx=80)

    # Функция для открытия диалога выбора файла
    def browse_file():
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("MS Excel", "*.xls;*.xlsx;*XLS;*XLSX")]
        )
        if file_path:
            file_label.config(text=file_path)

    # Кнопка для открытия диалога выбора файла
    browse_button = Button(file_frame, text="Выбрать файл", command=browse_file)
    browse_button.pack(side=LEFT)
    
    # Метка для отображения пути к выбранному файлу
    file_label = Label(file_frame, text=file_txt)
    file_label.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # УКАЗАНИЕ ДИСТРИБЬЮТОРА   ############################

    distributors_frame = Frame(data_edit_modal)
    distributors_frame.pack(pady=5, anchor='w', padx=80)

    distributors_label = Label(distributors_frame, text="Дистрибьютор: ")
    distributors_label.pack(side=LEFT)

    selected_distributor = StringVar(master)
    selected_distributor.set(distributor)

    with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
        dists_columns = json.load(file)

    distributors_list = list(dists_columns.keys())
    
    # Создание выпадающего списка
    distributors_dropdown = OptionMenu(distributors_frame, selected_distributor, *distributors_list)
    distributors_dropdown.config(width=20)
    distributors_dropdown.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # УКАЗАНИЕ ЛИСТА   ############################

    sheet_index_frame = Frame(data_edit_modal)
    sheet_index_frame.pack(pady=5, anchor='w', padx=80)

    sheet_index_label = Label(sheet_index_frame, text="Индекс листа (с нуля): ")
    sheet_index_label.pack(side=LEFT)

    sheet_index_entry = Entry(sheet_index_frame, width=5)
    sheet_index_entry.insert(0, sheet_index)
    data_edit_modal.focus_set()
    sheet_index_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # СТОЛБЕЦ НАИМЕНОВАНИЙ   ############################

    name_frame = Frame(data_edit_modal)
    name_frame.pack(pady=5, anchor='w', padx=80)

    name_label = Label(name_frame, text="Столбец наименований: ")
    name_label.pack(side=LEFT)

    name_entry = Entry(name_frame, width=5)
    name_entry.insert(0, name_column)
    data_edit_modal.focus_set()
    name_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # СТОЛБЕЦ НАЧАЛЬНОГО ОСТАТКА   ############################

    balance_beginning_frame = Frame(data_edit_modal)
    balance_beginning_frame.pack(pady=5, anchor='w', padx=80)

    balance_beginning_label = Label(balance_beginning_frame, text="Столбец остатков в начале: ")
    balance_beginning_label.pack(side=LEFT)

    balance_beginning_entry = Entry(balance_beginning_frame, width=5)
    balance_beginning_entry.insert(0, balance_beginning_column)
    data_edit_modal.focus_set()
    balance_beginning_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # СТОЛБЕЦ ПРИХОДА   ############################

    incomes_frame = Frame(data_edit_modal)
    incomes_frame.pack(pady=5, anchor='w', padx=80)

    incomes_label = Label(incomes_frame, text="Столбец приходов: ")
    incomes_label.pack(side=LEFT)

    incomes_entry = Entry(incomes_frame, width=5)
    incomes_entry.insert(0, incomes_column)
    data_edit_modal.focus_set()
    incomes_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # СТОЛБЕЦ ПРОДАЖ   ############################

    sold_number_frame = Frame(data_edit_modal)
    sold_number_frame.pack(pady=5, anchor='w', padx=80)

    sold_number_label = Label(sold_number_frame, text="Столбец продаж: ")
    sold_number_label.pack(side=LEFT)

    sold_number_entry = Entry(sold_number_frame, width=5)
    sold_number_entry.insert(0, sold_number_column)
    data_edit_modal.focus_set()
    sold_number_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # СТОЛБЕЦ КОНЕЧНОГО ОСТАТКА   ############################

    balance_end_frame = Frame(data_edit_modal)
    balance_end_frame.pack(pady=5, anchor='w', padx=80)

    balance_end_label = Label(balance_end_frame, text="Столбец конечных остатков: ")
    balance_end_label.pack(side=LEFT)

    balance_end_entry = Entry(balance_end_frame, width=5)
    balance_end_entry.insert(0, balance_end_column)
    data_edit_modal.focus_set()
    balance_end_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # СТРОКА НАЧАЛА   ############################

    start_row_frame = Frame(data_edit_modal)
    start_row_frame.pack(pady=5, anchor='w', padx=80)

    start_row_label = Label(start_row_frame, text="Начать со троки: ")
    start_row_label.pack(side=LEFT)

    start_row_entry = Entry(start_row_frame, width=5)
    start_row_entry.insert(0, start_row_number)
    data_edit_modal.focus_set()
    start_row_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # ЧЕКБОКС СОХРАНЕНИЯ ####################################

    save_data = BooleanVar()
    save_checkbutton = Checkbutton(
        data_edit_modal, 
        text="Сохранить данные дистрибьютора", 
        variable=save_data
    )

    if mode == "create":
        save_data.set(False)
        save_checkbutton.config(state="disabled")
    else:
        save_checkbutton.config(state="normal")

        with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
            dists_columns = json.load(file)

        cols_dict = dists_columns[selected_distributor.get()]['primary']
        save_data.set(bool(cols_dict["save"]))

    save_checkbutton.pack(pady=5)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # КНОПКИ ###################################################

    buttons_frame = Frame(data_edit_modal)
    buttons_frame.pack(pady=10, side=BOTTOM)

    # Функция проверки и сохранения данных
    def save_input():
        try:
            new_dist_file = DistributorsFilePrimary(
                filename = file_label.cget("text"),
                distributor=selected_distributor.get(),
                sheet_index=int(sheet_index_entry.get().replace(" ", "")),
                name_column=name_entry.get().replace(" ","") if name_entry.get().replace(" ","") != "" else None,
                balance_beginning_column=balance_beginning_entry.get().replace(" ","") if balance_beginning_entry.get().replace(" ","") != "" else None,
                incomes_column=incomes_entry.get().replace(" ","") if incomes_entry.get().replace(" ","") != "" else None,
                sold_number_column=sold_number_entry.get().replace(" ","") if sold_number_entry.get().replace(" ","") != "" else None,
                balance_end_column=balance_end_entry.get().replace(" ","") if balance_end_entry.get().replace(" ","") != "" else None,
                start_row_number=int(start_row_entry.get().replace(" ",""))
            )
            # print(new_dist_file.rendering_mode)
            new_dist_file.render()
            if mode == "create":                
                primary_input_dist_files.append(new_dist_file)
                input_listbox.insert(END, new_dist_file.filename)
            elif mode == "update":
                primary_input_dist_files[primary_selected_dist_file_index] = new_dist_file
                input_listbox.delete(primary_selected_dist_file_index)
                input_listbox.insert(primary_selected_dist_file_index, new_dist_file.filename)
            primary_selected_dist_file_index = None

            with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
                dists_columns = json.load(file)

            updated_dists_columns = dists_columns.copy()
            updated_dists_columns[selected_distributor.get()]['primary']["save"] = int(save_data.get())
            updated_dists_columns[selected_distributor.get()]['primary']["sheet_index"] = sheet_index_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['primary']["name_column"] = name_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['primary']["balance_beginning_column"] = balance_beginning_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['primary']["incomes_column"] = incomes_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['primary']["sold_number_column"] = sold_number_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['primary']["balance_end_column"] = balance_end_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['primary']["start_row_number"] = start_row_entry.get().replace(" ","")

            with open("json_files/dists_columns.json", 'w', encoding='utf-8') as file:
                json.dump(updated_dists_columns, file, ensure_ascii=False, indent=4)
                
            primary_current_rendered_file = None
            open_file_button.config(state="disabled")

            if input_listbox.size() > 0:
                render_button.config(state="normal")
            else:
                render_button.config(state="disabled")

            data_edit_modal.destroy()

        except Exception as err:
            messagebox.showerror("Ошибка ввода!", err)
            raise err
      

    # Кнопка для сохранения данных
    ok_button = Button(buttons_frame, text="ОК", width=10, command=save_input)
    ok_button.pack(pady=10, padx=20, side=LEFT)

    # Кнопка для закрытия модального окна
    close_button = Button(buttons_frame, text="Отмена", width=10, command=data_edit_modal.destroy)
    close_button.pack(pady=10, side=LEFT)

    # Кнопка удаления данных
    delete_button = Button(
        buttons_frame, 
        text="Удалить", 
        width=10, 
        state = "normal" if enable_delete_button else "disabled"
    )
    delete_button.pack(pady=10, padx=20)

    def change_distributor(*args):
        with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
            dists_columns = json.load(file)

        dist = selected_distributor.get()
        cols_dict = dists_columns[dist]['primary']

        save_checkbutton.config(state="normal")
        save_data.set(bool(cols_dict["save"]))


        if bool(cols_dict["save"]):
            sheet_index_entry.delete(0, END)
            sheet_index_entry.insert(0, cols_dict["sheet_index"])

            name_entry.delete(0, END)
            name_entry.insert(0, cols_dict["name_column"])

            balance_beginning_entry.delete(0, END)
            balance_beginning_entry.insert(0, cols_dict["balance_beginning_column"])

            incomes_entry.delete(0, END)
            incomes_entry.insert(0, cols_dict["incomes_column"])

            sold_number_entry.delete(0, END)
            sold_number_entry.insert(0, cols_dict["sold_number_column"])

            balance_end_entry.delete(0, END)
            balance_end_entry.insert(0, cols_dict["balance_end_column"])

            start_row_entry.delete(0, END)
            start_row_entry.insert(0, cols_dict["start_row_number"])

        else:
            sheet_index_entry.delete(0, END)
            name_entry.delete(0, END)
            balance_beginning_entry.delete(0, END)
            incomes_entry.delete(0, END)
            sold_number_entry.delete(0, END)
            balance_end_entry.delete(0, END)
            start_row_entry.delete(0, END)

            sheet_index_entry.insert(0, "0")
            start_row_entry.insert(0, "1")


        data_edit_modal.focus_set()


    selected_distributor.trace_add("write", change_distributor)


    # Ожидание закрытия модального окна
    master.wait_window(data_edit_modal)


















# ШАБЛОН ДЛЯ ВТРОИЧНЫХ ФАЙЛОВ

def open_secondary_template_modal(
        master,
        input_listbox,
        open_file_button,
        render_button,
        not_found_names_listbox,
        not_found_regions_listbox,
        secondary_selected_dist_file_index,
        secondary_current_rendered_file,
        secondary_input_dist_files,
        title = "Новые данные",
        file_txt = "Файл не выбран",
        distributor = "Не выбрано",
        sheet_index = "0",
        name_column = "",
        region1_column = "", 
        region2_column = "", 
        sold_number_column = "", 
        client_column = "", 
        start_row_number = "1",
        enable_delete_button = False,
        mode = "create",
    ):
    """
    Модальное окно для ввода шаблона вторичного файла
    """
    data_edit_modal = Toplevel(master)
    data_edit_modal.title(title)

    icon = PhotoImage(file='images/ReporterUI_Logo.png')
    data_edit_modal.iconphoto(False, icon)

    # Задание размера и позиции окна (ширинаxвысота+x+y)
    data_edit_modal.geometry("550x430+600+200")

    # Сделать окно модальным
    data_edit_modal.transient(master)  # Сделать его подчинённым к основному окну
    data_edit_modal.grab_set()  # Захватить все события до закрытия окна

    # Запретить изменение размера окна
    data_edit_modal.resizable(False, False)


    # УКАЗАНИЕ ФАЙЛА ############################

    file_frame = Frame(data_edit_modal)
    file_frame.pack(pady=5, anchor='w', padx=80)

    # Функция для открытия диалога выбора файла
    def browse_file():
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("MS Excel", "*.xls;*.xlsx;*XLS;*XLSX")]
        )
        if file_path:
            file_label.config(text=file_path)

    # Кнопка для открытия диалога выбора файла
    browse_button = Button(file_frame, text="Выбрать файл", command=browse_file)
    browse_button.pack(side=LEFT)
    
    # Метка для отображения пути к выбранному файлу
    file_label = Label(file_frame, text=file_txt)
    file_label.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




    # УКАЗАНИЕ ДИСТРИБЬЮТОРА   ############################

    distributors_frame = Frame(data_edit_modal)
    distributors_frame.pack(pady=5, anchor='w', padx=80)

    distributors_label = Label(distributors_frame, text="Дистрибьютор: ")
    distributors_label.pack(side=LEFT)

    selected_distributor = StringVar(master)
    selected_distributor.set(distributor)

    with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
        dists_columns = json.load(file)

    distributors_list = list(dists_columns.keys())
    
    # Создание выпадающего списка
    distributors_dropdown = OptionMenu(distributors_frame, selected_distributor, *distributors_list)
    distributors_dropdown.config(width=20)
    distributors_dropdown.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # УКАЗАНИЕ ЛИСТА   ############################

    sheet_index_frame = Frame(data_edit_modal)
    sheet_index_frame.pack(pady=5, anchor='w', padx=80)

    sheet_index_label = Label(sheet_index_frame, text="Индекс листа (с нуля): ")
    sheet_index_label.pack(side=LEFT)

    sheet_index_entry = Entry(sheet_index_frame, width=5)
    sheet_index_entry.insert(0, sheet_index)
    data_edit_modal.focus_set()
    sheet_index_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # СТОЛБЕЦ НАИМЕНОВАНИЙ   ############################

    name_frame = Frame(data_edit_modal)
    name_frame.pack(pady=5, anchor='w', padx=80)

    name_label = Label(name_frame, text="Столбец наименований: ")
    name_label.pack(side=LEFT)

    name_entry = Entry(name_frame, width=5)
    name_entry.insert(0, name_column)
    data_edit_modal.focus_set()
    name_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # СТОЛБЕЦ РЕГИОНОВ 1   ############################

    regions_1_frame = Frame(data_edit_modal)
    regions_1_frame.pack(pady=5, anchor='w', padx=80)

    regions_1_label = Label(regions_1_frame, text="Столбец регионов 1: ")
    regions_1_label.pack(side=LEFT)

    regions_1_entry = Entry(regions_1_frame, width=5)
    regions_1_entry.insert(0, region1_column)
    data_edit_modal.focus_set()
    regions_1_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # СТОЛБЕЦ РЕГИОНОВ 2   ############################

    regions_2_frame = Frame(data_edit_modal)
    regions_2_frame.pack(pady=5, anchor='w', padx=80)

    regions_2_label = Label(regions_2_frame, text="Столбец регионов 2: ")
    regions_2_label.pack(side=LEFT)

    regions_2_entry = Entry(regions_2_frame, width=5)
    regions_2_entry.insert(0, region2_column)
    data_edit_modal.focus_set()
    regions_2_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # СТОЛБЕЦ ПРОДАЖ   ############################

    sold_count_frame = Frame(data_edit_modal)
    sold_count_frame.pack(pady=5, anchor='w', padx=80)

    sold_count_label = Label(sold_count_frame, text="Столбец продаж: ")
    sold_count_label.pack(side=LEFT)

    sold_count_entry = Entry(sold_count_frame, width=5)
    sold_count_entry.insert(0, sold_number_column)
    data_edit_modal.focus_set()
    sold_count_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # СТОЛБЕЦ КЛИЕНТОВ   ############################

    clients_frame = Frame(data_edit_modal)
    clients_frame.pack(pady=5, anchor='w', padx=80)

    clients_label = Label(clients_frame, text="Столбец клиентов: ")
    clients_label.pack(side=LEFT)

    clients_entry = Entry(clients_frame, width=5)
    clients_entry.insert(0, client_column)
    data_edit_modal.focus_set()
    clients_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # СТРОКА НАЧАЛА   ############################

    start_row_frame = Frame(data_edit_modal)
    start_row_frame.pack(pady=5, anchor='w', padx=80)

    start_row_label = Label(start_row_frame, text="Начать со троки: ")
    start_row_label.pack(side=LEFT)

    start_row_entry = Entry(start_row_frame, width=5)
    start_row_entry.insert(0, start_row_number)
    data_edit_modal.focus_set()
    start_row_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    
    # СТРОКА КОНЦА   ############################

    # last_row_frame = Frame(data_edit_modal)
    # last_row_frame.pack(pady=5, anchor='w', padx=80)

    # last_row_label = Label(last_row_frame, text="Последняя строка: ")
    # last_row_label.pack(side=LEFT)

    # last_row_entry = Entry(last_row_frame, width=5)
    # last_row_entry.insert(0, last_row_number)
    # data_edit_modal.focus_set()
    # last_row_entry.pack()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # ЧЕКБОКС СОХРАНЕНИЯ ####################################

    save_data = BooleanVar()
    save_checkbutton = Checkbutton(
        data_edit_modal, 
        text="Сохранить данные дистрибьютора", 
        variable=save_data
    )

    if mode == "create":
        save_data.set(False)
        save_checkbutton.config(state="disabled")
    else:
        save_checkbutton.config(state="normal")

        with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
            dists_columns = json.load(file)

        cols_dict = dists_columns[selected_distributor.get()]['secondary']
        save_data.set(bool(cols_dict["save"]))

    save_checkbutton.pack(pady=5)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    buttons_frame = Frame(data_edit_modal)
    buttons_frame.pack(pady=10, side=BOTTOM)

    # Функция проверки и сохранения данных
    def save_input():
        try:
            new_dist_file = DistributorsFileSecondary(
                filename = file_label.cget("text"),
                distributor=selected_distributor.get(),
                sheet_index=int(sheet_index_entry.get().replace(" ", "")),
                name_column=name_entry.get().replace(" ","") if name_entry.get().replace(" ","") != "" else None,
                region1_column=regions_1_entry.get().replace(" ","") if regions_1_entry.get().replace(" ","") != "" else None,
                region2_column=regions_2_entry.get().replace(" ","") if regions_2_entry.get().replace(" ","") != "" else None,
                sold_number_column=sold_count_entry.get().replace(" ","") if sold_count_entry.get().replace(" ","") != "" else None,
                client_column=clients_entry.get().replace(" ","") if clients_entry.get().replace(" ","") != "" else None,
                start_row_number=int(start_row_entry.get().replace(" ",""))
            )
            # print(new_dist_file.rendering_mode)
            new_dist_file.render()
            if mode == "create":                
                secondary_input_dist_files.append(new_dist_file)
                input_listbox.insert(END, new_dist_file.filename)
            elif mode == "update":
                # global SECONDARY_SELECTED_DIST_FILE_INDEX
                secondary_input_dist_files[secondary_selected_dist_file_index] = new_dist_file
                input_listbox.delete(secondary_selected_dist_file_index)
                input_listbox.insert(secondary_selected_dist_file_index, new_dist_file.filename)
            secondary_selected_dist_file_index = None

            with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
                dists_columns = json.load(file)

            updated_dists_columns = dists_columns.copy()
            updated_dists_columns[selected_distributor.get()]['secondary']["save"] = int(save_data.get())
            updated_dists_columns[selected_distributor.get()]['secondary']["sheet_index"] = sheet_index_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['secondary']["name_column"] = name_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['secondary']["region1_column"] = regions_1_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['secondary']["region2_column"] = regions_2_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['secondary']["sold_number_column"] = sold_count_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['secondary']["client_column"] = clients_entry.get().replace(" ","")
            updated_dists_columns[selected_distributor.get()]['secondary']["start_row_number"] = start_row_entry.get().replace(" ","")

            with open("json_files/dists_columns.json", 'w', encoding='utf-8') as file:
                json.dump(updated_dists_columns, file, ensure_ascii=False, indent=4)
            
            # global SECONDARU_CURRENT_RENDERED_FILE
            secondary_current_rendered_file = None
            open_file_button.config(state="disabled")

            if input_listbox.size() > 0:
                render_button.config(state="normal")
            else:
                render_button.config(state="disabled")

            data_edit_modal.destroy()

        except Exception as err:
            messagebox.showerror("Ошибка ввода!", err)
            raise err
            

    # Кнопка для сохранения данных
    ok_button = Button(buttons_frame, text="ОК", width=10, command=save_input)
    ok_button.pack(pady=10, padx=20, side=LEFT)

    # Кнопка для закрытия модального окна
    close_button = Button(buttons_frame, text="Отмена", width=10, command=data_edit_modal.destroy)
    close_button.pack(pady=10, side=LEFT)

    def delete_data(
            secondary_selected_dist_file_index,
            secondary_current_rendered_file,
            secondary_input_dist_files
    ):
        # global SECONDARY_SELECTED_DIST_FILE_INDEX, SECONDARY_CURRENT_RENDERED_FILE
        print(secondary_selected_dist_file_index)
        input_listbox.delete(secondary_selected_dist_file_index)
        secondary_input_dist_files.pop(secondary_selected_dist_file_index)
        secondary_selected_dist_file_index = None
        not_found_names_listbox.delete(0,END)
        not_found_regions_listbox.delete(0,END)
        secondary_current_rendered_file = None
        open_file_button.config(state="disabled")

        if input_listbox.size() > 0:
            render_button.config(state="normal")
        else:
            render_button.config(state="disabled")

        data_edit_modal.destroy()


    # Кнопка удаления данных
    delete_button = Button(
        buttons_frame, 
        text="Удалить", 
        width=10, 
        state = "normal" if enable_delete_button else "disabled", 
        command=lambda:delete_data(
            secondary_selected_dist_file_index,
            secondary_current_rendered_file,
            secondary_input_dist_files
            )
    )
    delete_button.pack(pady=10, padx=20)

    def change_distributor(*args):

        with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
            dists_columns = json.load(file)

        dist = selected_distributor.get()
        cols_dict = dists_columns[dist]['secondary']

        save_checkbutton.config(state="normal")
        save_data.set(bool(cols_dict["save"]))


        if bool(cols_dict["save"]):
            sheet_index_entry.delete(0, END)
            sheet_index_entry.insert(0, cols_dict["sheet_index"])

            name_entry.delete(0, END)
            name_entry.insert(0, cols_dict["name_column"])

            regions_1_entry.delete(0, END)
            regions_1_entry.insert(0, cols_dict["region1_column"])

            regions_2_entry.delete(0, END)
            regions_2_entry.insert(0, cols_dict["region2_column"])

            sold_count_entry.delete(0, END)
            sold_count_entry.insert(0, cols_dict["sold_number_column"])

            clients_entry.delete(0, END)
            clients_entry.insert(0, cols_dict["client_column"])

            start_row_entry.delete(0, END)
            start_row_entry.insert(0, cols_dict["start_row_number"])

        else:
            sheet_index_entry.delete(0, END)
            name_entry.delete(0, END)
            regions_1_entry.delete(0, END)
            regions_2_entry.delete(0, END)
            sold_count_entry.delete(0, END)
            clients_entry.delete(0, END)
            start_row_entry.delete(0, END)

            sheet_index_entry.insert(0, "0")
            start_row_entry.insert(0, "1")


        data_edit_modal.focus_set()


    selected_distributor.trace_add("write", change_distributor)


    # Ожидание закрытия модального окна
    master.wait_window(data_edit_modal)



# РЕДАКТИРОВАНИЕ БАЗЫ ДАННЫХ

def open_edit_employee_modal(
        master,
        employees_treeview,
        new=True,
        name = "",
        group = "Выберите группу",
        current_regions = []
    ):
        
        original_data_name = name
        original_data_group = group
        original_data_regions = current_regions

        edit_employee_modal = Toplevel(master)
        edit_employee_modal.title("Новый сотрудник" if new else "Редактировать сотрудника")

        icon = PhotoImage(file='images/ReporterUI_Logo.png')
        edit_employee_modal.iconphoto(False, icon)

        edit_employee_modal.geometry("480x350+630+240")

        # Запретить изменение размера окна
        edit_employee_modal.resizable(False, False)

        # Сделать окно модальным
        edit_employee_modal.transient(master)
        edit_employee_modal.grab_set()

        edit_employee_modal.focus_set()

        # Проверить заполненность и изменить состояние кнопки "Сохранить"
        def check_fullness(*args):
            if len(name_entry.get()) and selected_group.get() in db.get_groups() and len(regions_listbox.get(0,END)):                
                save_button.config(state="normal")
            else:
                save_button.config(state="disabled")


        # NAME 
        name_frame = Frame(edit_employee_modal, width=500)
        name_frame.pack(pady=20)

        name_label = Label(name_frame, text="Ф.И.О.:")
        name_label.pack(side=LEFT, anchor='w')

        name_entry = Entry(name_frame, width=30)
        name_entry.pack(side=RIGHT, anchor='e')

        name_entry.bind('<KeyRelease>', check_fullness)

        name_entry.insert(0, name)

        name_entry.bind()

        # GROUP
        group_frame = Frame(edit_employee_modal, width=500)
        group_frame.pack(pady=10)

        group_label = Label(group_frame, text="Группа:")
        group_label.pack(side=LEFT, anchor='w')

        selected_group = StringVar(edit_employee_modal)
        selected_group.set(group)

        selected_group.trace_add('write', check_fullness)

        groups_list = db.get_groups()
        group_menu = OptionMenu(group_frame, selected_group, *groups_list)
        group_menu.config(width=20)
        group_menu.pack()


        # REGION ADDITION
        region_addition_frame = Frame(edit_employee_modal, width=500)
        region_addition_frame.pack(pady=10)

        region_addition_label = Label(region_addition_frame, text="Добавить регион:")
        region_addition_label.pack(side=LEFT, anchor='w')

        selected_region = StringVar(edit_employee_modal)
        selected_region.set("Выберите новый регион")

        global regions_list
        regions_list = db.get_all_regions()

        for reg in current_regions:
            if reg in regions_list:
                regions_list.remove(reg)

        regions_menu = OptionMenu(region_addition_frame, selected_region, *regions_list)
        regions_menu.config(width=30)
        regions_menu.pack(side=LEFT, anchor='w')

        def enable_add_region_button(*args):
            add_region_button.config(state="normal")

        selected_region.trace_add('write', enable_add_region_button)

        def add_new_region():
            selected_region_str = selected_region.get()
            regions_listbox.insert(END, selected_region_str)
            global regions_list
            regions_list.remove(selected_region_str)
            regions_menu['menu'].delete(0,END)
            for reg in regions_list:
                regions_menu['menu'].add_command(label=reg, command=lambda value=reg: selected_region.set(value))
            selected_region.set("Выберите новый регион")
            add_region_button.config(state="disabled")
            check_fullness()

        add_region_button = Button(region_addition_frame, text="Добавить", state="disabled", command=add_new_region)
        add_region_button.config(width=8)
        add_region_button.pack(side=LEFT, anchor='w', padx=5)

        # CURRENT REGIONS LIST
        regions_listbox_frame = Frame(edit_employee_modal, width=450, height=100)
        regions_listbox_frame.pack()

        regions_listbox_scrollbar = Scrollbar(regions_listbox_frame)

        regions_listbox = Listbox(regions_listbox_frame, width=50, height=7, yscrollcommand=regions_listbox_scrollbar.set)
        regions_listbox.pack(side=LEFT, fill=Y)


        def remove_region(index):
            regions_listbox.delete(index)
            regions_menu["menu"].delete(0, END)

            global regions_list
            regions_list = db.get_all_regions()
            current_regions = regions_listbox.get(0,END)
            for curreg in current_regions:
                if curreg in regions_list:
                    regions_list.remove(curreg)

            for reg in regions_list:
                regions_menu['menu'].add_command(label=reg, command=lambda value=reg: selected_region.set(value))
            
            remove_region_button.config(state="disabled")
            check_fullness()


        def on_regions_listbox_select(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                remove_region_button.config(state="normal", command=lambda index=index: remove_region(index))
        
        regions_listbox.bind('<<ListboxSelect>>', on_regions_listbox_select)
        regions_listbox.bind('<FocusOut>', lambda event: remove_region_button.config(state="disabled"))

        for cur_reg in current_regions:
            regions_listbox.insert(END, cur_reg)

        regions_listbox_scrollbar.pack(side=LEFT, fill=Y)
        regions_listbox_scrollbar.config(command=regions_listbox.yview)

        remove_region_button = Button(regions_listbox_frame, text="Убрать", state="disabled")
        remove_region_button.pack(side=LEFT)

        # "SAVE", "CANCEL" AND "DELETE" BUTTONS
        buttons_frame = Frame(edit_employee_modal, width=450)
        buttons_frame.pack(pady=20)

        def save():
            with open("json_files/employees.json", 'r', encoding='utf-8') as file:
                employees = json.load(file)
            
            if not new:
                employees.remove(
                    {
                        "name": original_data_name,
                        "group": original_data_group,
                        "regions": original_data_regions
                    }
                )
                
                for item in employees_treeview.get_children():
                    item_values = employees_treeview.item(item, 'values')
                    if item_values == (original_data_name, original_data_group, ';'.join(original_data_regions)):
                        employees_treeview.delete(item)
                        break

            data_name = name_entry.get()
            data_group = selected_group.get()
            data_regions = regions_listbox.get(0, END)

            employees.append(
                {
                    "name": data_name,
                    "group": data_group,
                    "regions": data_regions
                }
            )
            
            with open("json_files/employees.json", 'w', encoding='utf-8') as file:
                json.dump(employees, file, ensure_ascii=False, indent=4)

            
            
            employees_treeview.insert('', 
                            END, 
                            values=(data_name, 
                                    data_group, 
                                    ';'.join(data_regions)
                                    )
                            )
            
            edit_employee_modal.destroy()

        save_button = Button(buttons_frame, text="Сохранить", state="disabled", command=save)
        save_button.pack(side=LEFT, padx=10)

        cancel_button = Button(buttons_frame, text="Отмена", command=lambda:edit_employee_modal.destroy())
        cancel_button.pack(side=LEFT, padx=10)

        def delete():
            with open("json_files/employees.json", 'r', encoding='utf-8') as file:
                employees = json.load(file)
            
            employees.remove(
                {
                    "name": original_data_name,
                    "group": original_data_group,
                    "regions": original_data_regions
                }
            )
            
            with open("json_files/employees.json", 'w', encoding='utf-8') as file:
                json.dump(employees, file, ensure_ascii=False, indent=4)
            
            for item in employees_treeview.get_children():
                    item_values = employees_treeview.item(item, 'values')
                    if item_values == (original_data_name, original_data_group, ';'.join(original_data_regions)):
                        employees_treeview.delete(item)
                        break
            
            edit_employee_modal.destroy()

        
        delete_button = Button(
            buttons_frame, text="Удалить сотрудника", state="disabled" if new else "normal", command=delete
        )
        delete_button.pack(padx=15)

        check_fullness()


def open_edit_distributor_modal(
        master,
        distributors_listbox,
        new=True,
        name:str=""
):
    original_name = name

    edit_distributor_modal = Toplevel(master)
    edit_distributor_modal.title("Новый дистрибьютор" if new else "Редактировать дистрибьютор")

    icon = PhotoImage(file='images/ReporterUI_Logo.png')
    edit_distributor_modal.iconphoto(False, icon)

    edit_distributor_modal.geometry("480x200+630+340")

    # Запретить изменение размера окна
    edit_distributor_modal.resizable(False, False)

    # Сделать окно модальным
    edit_distributor_modal.transient(master)
    edit_distributor_modal.grab_set()

    edit_distributor_modal.focus_set()

    name_entry_var = StringVar()

    name_entry = Entry(edit_distributor_modal, width=20, textvariable=name_entry_var, font=("Arial", 12))
    name_entry.insert(END, name)
    name_entry.pack(pady=20)



    # Функция "Сохранить"
    def save():
        with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
            dists_columns = json.load(file)
        
        if not new:
            dists_columns.pop(original_name)
            index = distributors_listbox.get(0, END).index(original_name)
            distributors_listbox.delete(index)
            

        data_name = name_entry.get()

        dists_columns[data_name] = {
            "primary": {
                "save": 1,
                "sheet_index": "0",
                "name_column": "",
                "balance_beginning": "",
                "incomes": "",
                "sold_number": "",
                "balance_end": ""
                    },
            "secondary": {
                "save": 0,
                "sheet_index": "",
                "name_column": "",
                "region1_column": "",
                "region2_column": "",
                "sold_number_column": "",
                "client_column": "",
                "start_row_number": "",
                "last_row_number": ""
            }
        }
        
        with open("json_files/dists_columns.json", 'w', encoding='utf-8') as file:
            json.dump(dists_columns, file, ensure_ascii=False, indent=4)

        
        
        distributors_listbox.insert(END, data_name)
        
        edit_distributor_modal.destroy()

    # Функция "Удалить"
    def delete():
        with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
            dists_columns = json.load(file)
        
        dists_columns.pop(original_name)
        
        with open("json_files/dists_columns.json", 'w', encoding='utf-8') as file:
            json.dump(dists_columns, file, ensure_ascii=False, indent=4)
        
        index = distributors_listbox.get(0, END).index(original_name)
        distributors_listbox.delete(index)
        
        edit_distributor_modal.destroy()


    # Фрейм кнопок
    buttons_frame = Frame(edit_distributor_modal, width=450)
    buttons_frame.pack(pady=20)

    # Кнопка "Сохранить"
    save_button = Button(buttons_frame, text="Сохранить", state="disabled", command=save)
    save_button.pack(side=LEFT, padx=10)

    # Кнопка "Отмена"
    cancel_button = Button(buttons_frame, text="Отмена", command=lambda:edit_distributor_modal.destroy())
    cancel_button.pack(side=LEFT, padx=10)

    # Кнопка "Удалить"
    delete_button = Button(
        buttons_frame, text="Удалить дистрибютор", state="disabled" if new else "normal", command=delete
    )
    delete_button.pack(padx=15)

    def on_name_entry_change(*args):

        with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
            dists_columns = json.load(file)
            distributors_list = list(dists_columns.keys())

        if name_entry_var.get() == "" or name_entry_var.get() in distributors_list:
            save_button.config(state="disabled")
        else:
            save_button.config(state="normal")
    
    name_entry_var.trace_add('write', on_name_entry_change)
    

def open_edit_name_modal(
        master,
        names_treeview,
        new=True,
        name="",
        producer="Выберите производителя",
        group="Выберите группу",
        price=""
):
    original_name = name
    original_producer = producer
    original_group = group
    original_price = price

    edit_name_modal = Toplevel(master)
    edit_name_modal.title("Новое наименование" if new else "Редактировать наименование")

    icon = PhotoImage(file='images/ReporterUI_Logo.png')
    edit_name_modal.iconphoto(False, icon)

    edit_name_modal.geometry("480x350+630+240")

    # Запретить изменение размера окна
    edit_name_modal.resizable(False, False)

    # Сделать окно модальным
    edit_name_modal.transient(master)
    edit_name_modal.grab_set()

    edit_name_modal.focus_set()

    # Проверить заполненность и изменить состояние кнопки "Сохранить"
    def check_fullness(*args):
        # pass
        if len(name_entry.get()) and \
        selected_producer.get() in db.get_all_producers() and \
        selected_group.get() in db.get_groups() and \
        price_entry.get().count(",")<=1 and \
        str.isdigit(price_entry.get().replace(",","")):
            save_button.config(state="normal")
        else:
            save_button.config(state="disabled")

    Frame(edit_name_modal, height=20).pack()

    # NAME 
    name_frame = Frame(edit_name_modal, width=500)
    name_frame.pack(pady=20)

    name_label = Label(name_frame, text="Наименование:")
    name_label.pack(side=LEFT, anchor='w')

    name_entry = Entry(name_frame, width=50)
    name_entry.pack(side=RIGHT, anchor='e')

    name_entry.bind('<KeyRelease>', check_fullness)

    name_entry.insert(0, name)

    name_entry.bind()

    # PRODUCER
    producer_frame = Frame(edit_name_modal, width=500)
    producer_frame.pack(pady=10)

    producer_label = Label(producer_frame, text="Производитель:")
    producer_label.pack(side=LEFT, anchor='w')

    selected_producer = StringVar(edit_name_modal)
    selected_producer.set(producer)

    selected_producer.trace_add('write', check_fullness)

    producers_list = db.get_all_producers()
    producer_menu = OptionMenu(producer_frame, selected_producer, *producers_list)
    producer_menu.config(width=25)
    producer_menu.pack()

    # GROUP
    group_frame = Frame(edit_name_modal, width=500)
    group_frame.pack(pady=10)

    group_label = Label(group_frame, text="Группа:")
    group_label.pack(side=LEFT, anchor='w')

    selected_group = StringVar(edit_name_modal)
    selected_group.set(group)

    selected_group.trace_add('write', check_fullness)

    groups_list = db.get_groups()
    group_menu = OptionMenu(group_frame, selected_group, *groups_list)
    group_menu.config(width=20)
    group_menu.pack()

    # PRICE 
    price_frame = Frame(edit_name_modal, width=500)
    price_frame.pack(pady=20)

    price_label = Label(price_frame, text="Цена:")
    price_label.pack(side=LEFT, anchor='w')

    price_entry = Entry(price_frame, width=10)
    price_entry.pack(side=RIGHT, anchor='e')

    price_entry.bind('<KeyRelease>', check_fullness)

    price_entry.insert(0, price)

    price_entry.bind()

    # "SAVE", "CANCEL" AND "DELETE" BUTTONS
    buttons_frame = Frame(edit_name_modal, width=450)
    buttons_frame.pack(pady=20)

    def save():
        if new:
            db.insert_new_general_name(
                name_entry.get(),
                price_entry.get(),
                selected_group.get(),
                selected_producer.get()
            )
            names_treeview.insert(
                '',
                END,
                values=(name_entry.get(),
                        selected_producer.get(),
                        selected_group.get(),
                        price_entry.get()
                        )
            )
            edit_name_modal.destroy()
        else:
            db.update_general_name(
                original_name,
                name_entry.get(),
                selected_producer.get(),
                selected_group.get(),
                price_entry.get()
            )
            for item_id in names_treeview.get_children():
                values = names_treeview.item(item_id, "values")
                if values == (original_name, original_producer, original_group, original_price):
                    names_treeview.delete(item_id)
                    names_treeview.insert(
                        '',
                        END,
                        values=(name_entry.get(),
                                selected_producer.get(),
                                selected_group.get(),
                                price_entry.get()
                                ) 
                        )
                    break
            edit_name_modal.destroy()

    save_button = Button(buttons_frame, text="Сохранить", state="disabled", command=save)
    save_button.pack(side=LEFT, padx=10)

    cancel_button = Button(buttons_frame, text="Отмена", command=lambda:edit_name_modal.destroy())
    cancel_button.pack(side=LEFT, padx=10)

    def delete():
        db.delete_general_name(original_name)
        for item_id in names_treeview.get_children():
            values = names_treeview.item(item_id, "values")
            if values == (original_name, original_producer, original_group, original_price):
                names_treeview.delete(item_id)
                break
        edit_name_modal.destroy()
        

    delete_button = Button(
        buttons_frame, text="Удалить наименование", state="disabled" if new else "normal", command=delete
    )
    delete_button.pack(padx=15)

    check_fullness()


def open_database_modal(master):
    database_modal = Toplevel(master)
    database_modal.title("База данных")

    icon = PhotoImage(file='images/ReporterUI_Logo.png')
    database_modal.iconphoto(False, icon)

    database_modal.geometry("550x430+600+200")

    # Запретить изменение размера окна
    database_modal.resizable(False, False)

    # Сделать окно модальным
    database_modal.transient(master)
    database_modal.grab_set()

    database_modal.focus_set()

    # Виджет Notebook для вкладок
    notebook = ttk.Notebook(database_modal)

    # Создаем вкладки
    employees_tab = ttk.Frame(notebook)
    distributors_tab = ttk.Frame(notebook)
    groups_tab = ttk.Frame(notebook)
    names_tab = ttk.Frame(notebook)
    regions_tab = ttk.Frame(notebook)


    # Добавляем влкадки в виджет
    notebook.add(employees_tab, text="Сотрудники")
    notebook.add(distributors_tab, text="Дистрибьюторы")
    notebook.add(names_tab, text="Наименования")

    # Упаковываем Notebook
    notebook.pack(expand=True, fill='both')

    # СОДЕРЖИМОЕ:

    # Сотрудники
    
    employees_label = Label(employees_tab, text="Сотрудники", font=('Arial', 12, 'bold'))
    employees_label.pack(pady=10)

    employees_treeview_frame = Frame(employees_tab, width=500, height=300, background="lightgrey")
    employees_treeview_frame.pack()

    # Создаем Treeview с тремя столбцами
    employees_treeview = ttk.Treeview(employees_treeview_frame, 
                                      columns=('name_col', 'group_col', 'region_col'), 
                                      show='headings',
                                      height=14
                                      )
    
    # # Определяем заголовки для столбцов
    employees_treeview.heading('name_col', text='ФИО')
    employees_treeview.heading('group_col', text='Группа')
    employees_treeview.heading('region_col', text='Регион')

    # # Задаем ширину столбцов
    employees_treeview.column('name_col', width=200)
    employees_treeview.column('group_col', width=100)
    employees_treeview.column('region_col', width=200)
    
    # Создаем вертикальную полосу прокрутки
    employees_treeview_scrollbar = ttk.Scrollbar(employees_treeview_frame, 
                                                 orient=VERTICAL, 
                                                 command=employees_treeview.yview
                                                 )
    employees_treeview.configure(yscrollcommand=employees_treeview_scrollbar.set)

    employees_treeview.pack(side=LEFT, fill=BOTH, expand=True)
    employees_treeview_scrollbar.pack(side=RIGHT, fill=Y)

    # # Добавляем данные в виде строк
    with open("json_files/employees.json", 'r', encoding='utf-8') as file:
        employees = json.load(file)
    
    for employee in employees:
        employees_treeview.insert('', 
                                  END, 
                                  values=(employee["name"], 
                                          employee["group"], 
                                          ';'.join(employee["regions"])
                                          )
                                  )
            
    def on_employee_click(event):
        selected_item = employees_treeview.focus()
        item_values = employees_treeview.item(selected_item, 'values')
        name = item_values[0]
        group = item_values[1]
        regions = item_values[2].split(";")
        open_edit_employee_modal(
            database_modal,
            employees_treeview,
            new=False,
            name=name,
            group=group,
            current_regions=regions
        )


    employees_treeview.bind("<Double-1>", on_employee_click)


    add_employee_button = Button(employees_tab, 
                                 text="Добавить", 
                                 command=lambda:open_edit_employee_modal(database_modal, employees_treeview)
                                 )
    add_employee_button.pack(pady=10)


    # Дистрибьюторы
    distributors_label = Label(distributors_tab, text="Дистрибьюторы", font=('Arial', 12, 'bold'))
    distributors_label.pack(pady=10)

    distributors_listbox_frame = Frame(distributors_tab, width=500, height=300, background="lightgrey")
    distributors_listbox_frame.pack()

    distributors_listbox = Listbox(distributors_listbox_frame, width=40, height=15, font=('Arial', 12))

    # Создаем вертикальную полосу прокрутки
    distributors_listbox_scrollbar = ttk.Scrollbar(distributors_listbox_frame, 
                                                 orient=VERTICAL, 
                                                 command=distributors_listbox.yview
                                                 )
    distributors_listbox.configure(yscrollcommand=distributors_listbox_scrollbar.set)

    distributors_listbox.pack(side=LEFT, fill=BOTH, expand=True)
    distributors_listbox_scrollbar.pack(side=RIGHT, fill=Y)

    # # Добавляем данные в виде строк
    with open("json_files/dists_columns.json", 'r', encoding='utf-8') as file:
        dists_columns = json.load(file)
    
    distributors = list(dists_columns.keys())

    for dist in distributors:
        distributors_listbox.insert(END, dist)  

    def on_dist_click(event):
        index = distributors_listbox.curselection()
        value = str(distributors_listbox.get(index))
        open_edit_distributor_modal(
            database_modal,
            distributors_listbox,
            new=False,
            name=value
        )
    

    distributors_listbox.bind("<Double-1>", on_dist_click)


    add_dist_button = Button(
        distributors_tab, text="Добавить", 
        command=lambda:open_edit_distributor_modal(database_modal, distributors_listbox)
    )
    add_dist_button.pack(pady=10)

    # Наименования
    names_label = Label(names_tab, text="Наименования", font=('Arial', 12, 'bold'))
    names_label.pack(pady=10)

    names_treeview_frame = Frame(names_tab, width=500, height=300, background="lightgrey")
    names_treeview_frame.pack()

    # Создаем Treeview с тремя столбцами
    names_treeview = ttk.Treeview(names_treeview_frame, 
                                      columns=('name_col', 'producer_col', 'group_col', 'price_col'), 
                                      show='headings',
                                      height=14
                                      )
    
    # # Определяем заголовки для столбцов
    names_treeview.heading('name_col', text='Наименование')
    names_treeview.heading('producer_col', text='Производитель')
    names_treeview.heading('group_col', text='Группа')
    names_treeview.heading('price_col', text='Цена')   

    # # Задаем ширину столбцов
    names_treeview.column('name_col', width=200)
    names_treeview.column('producer_col', width=100)
    names_treeview.column('group_col', width=100)
    names_treeview.column('price_col', width=100)

    # Загружаем наименования из БД
    names_data = db.get_names_data()

    # вводим загруженные данные в treeview
    for data in names_data:
        names_treeview.insert(
            '',
            END,
            values=tuple(data)
        )
    
    
    # Создаем вертикальную полосу прокрутки
    names_treeview_scrollbar = ttk.Scrollbar(names_treeview_frame, 
                                                 orient=VERTICAL, 
                                                 command=names_treeview.yview
                                                 )
    names_treeview.configure(yscrollcommand=names_treeview_scrollbar.set)

    names_treeview.pack(side=LEFT, fill=BOTH, expand=True)
    names_treeview_scrollbar.pack(side=RIGHT, fill=Y)


    def on_name_click(event):
        selected_item = names_treeview.focus()
        item_values = names_treeview.item(selected_item, 'values')
        name = item_values[0]
        producer = item_values[1]
        group = item_values[2]
        price = item_values[3]
        open_edit_name_modal(
            database_modal,
            names_treeview,
            new=False,
            name=name,
            producer=producer,
            group=group,
            price=price
        )
        # open_edit_employee_modal(
        #     database_modal,
        #     employees_treeview,
        #     new=False,
        #     name=name,
        #     group=group,
        #     current_regions=regions
        # )


    names_treeview.bind("<Double-1>", on_name_click)


    add_name_button = Button(names_tab,
                             text="Добавить",
                             command=lambda:open_edit_name_modal(database_modal, names_treeview)
                             )
    add_name_button.pack(pady=10)



# ВВЕДЕНИЕ НОВЫХ НЕИЗВЕСТНЫХ НАИМЕНОВАНИЙ ИЛИ РЕГИОНОВ

def open_insert_modal(        
        event,
        master,
        open_file_button,
        insert_mode:str,
        listbox_object
):
    index = listbox_object.curselection()[0]
    # print(index)
    # print(insert_mode)
    value = listbox_object.get(index)

    insert_modal = Toplevel(master)
    insert_modal.title("Новый регион" if insert_mode=="region" else "Новое наименование")

    icon = PhotoImage(file='images/ReporterUI_Logo.png')
    insert_modal.iconphoto(False, icon)

    # Задание размера и позиции окна (ширинаxвысота+x+y)
    insert_modal.geometry("550x300+550+250")

    # Сделать окно модальным
    insert_modal.transient(master)  # Сделать его подчинённым к основному окну
    insert_modal.grab_set()  # Захватить все события до закрытия окна

    # Запретить изменение размера окна
    insert_modal.resizable(False, False)

    # Сфокусируем на модальное окно
    insert_modal.focus_set()

    title_label = Label(
        insert_modal, 
        text="Ввод нового региона" if insert_mode=="region" else "Ввод нового наименования", 
        font=("Arial", 12, "bold")
    )
    title_label.pack(pady=20)
    
    Label(insert_modal, text=value, wraplength=200).pack(pady=10)

    def enable_save_button(event):
        save_button.config(state="normal")

    if insert_mode == "region":
        regions_list = db.get_all_regions()

        selected_region = StringVar(insert_modal)
        selected_region.set("Выберите соответствующий регион")
        regions_menu = OptionMenu(insert_modal, selected_region, *regions_list, command=enable_save_button)
        regions_menu.config(width=35)
        regions_menu.pack(pady=10)

    elif insert_mode == "name":
        names_list = db.get_all_names(sort_by_group=False)

        selected_name = StringVar(insert_modal)
        selected_name.set("Не выбрано")

        selected_name_label = Label(insert_modal, text=selected_name.get())
        selected_name_label.pack(pady=10)

        def show_names_menu():
            names_menu = Toplevel(insert_modal)
            names_menu.geometry("300x200+700+400")
            
            names_menu.title("Выбор наименования")
            icon = PhotoImage(file='images/ReporterUI_Logo.png')
            names_menu.iconphoto(False, icon)


            names_menu.transient(insert_modal)
            names_menu.grab_set()

            
            
            scrollbar = Scrollbar(names_menu)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            names_menu_listbox = Listbox(names_menu, yscrollcommand=scrollbar.set, selectmode=SINGLE)
            names_menu_listbox.pack(fill=BOTH, expand=True)

            scrollbar.config(command=names_menu_listbox.yview)

            for name in names_list:
                names_menu_listbox.insert(END, name)
            
            def select_name(event):
                selection = names_menu_listbox.curselection()
                if selection:
                    index = selection[0]
                    value = names_menu_listbox.get(index)
                    selected_name.set(value)  # Устанавливаем выбранное значение в основное поле
                    names_menu.destroy()
                    selected_name_label.config(text=value)
                    save_button.config(state="normal")

            names_menu_listbox.bind("<<ListboxSelect>>", select_name)
        
        dropdown_button = Button(insert_modal, text="Выбрать наименование", width=20, command=show_names_menu)
        dropdown_button.pack(pady=10)




        # selected_name = StringVar(insert_modal)
        # selected_name.set("Выберите соответствующее наименование")
        # names_menu = OptionMenu(insert_modal, selected_name, *names_list, command=enable_save_button)
        # names_menu.config(width=35)
        # names_menu.pack(pady=10)
    
    buttons_frame = Frame(insert_modal)
    buttons_frame.pack(pady=10)

    def insert_data():
        if insert_mode == "region":
            db.insert_unique_region(value, selected_region.get())
            listbox_object.delete(index)
        elif insert_mode == "name":
            db.insert_unique_name(value, selected_name.get())
            listbox_object.delete(index)
        
        global CURRENT_RENDERED_FILE
        CURRENT_RENDERED_FILE = None
        open_file_button.config(state="disabled")

        insert_modal.destroy()

    def close_modal():
        insert_modal.destroy()

    save_button = Button(buttons_frame, text="Сохранить", width=10, state="disabled", command=insert_data)
    save_button.pack(pady=10, padx=15, side=LEFT)

    cancel_button = Button(buttons_frame, text="Отмена", width=10, command=close_modal)
    cancel_button.pack(pady=10, padx=15)

    
    




    # file_frame = Frame(insert_modal)
    # file_frame.pack(pady=5, anchor='w', padx=80)
