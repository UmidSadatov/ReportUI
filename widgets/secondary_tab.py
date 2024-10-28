from tkinter import *
from tkinter import filedialog, messagebox, ttk
from reporter import *
from datetime import datetime
import os

from .toplevels import *

SECONDARY_INPUT_DIST_FILES = []

SECONDARY_SELECTED_DIST_FILE_INDEX = None

SECONDARY_CURRENT_RENDERED_FILE = None

# ВТОРИЧНЫЙ ОТЧЕТ

def pack_secondary_main_frame(root, secondary_tab:ttk.Frame):
    secondary_main_frame = Frame(secondary_tab, width=1000, height=500, background="lightgrey")
    secondary_main_frame.pack_propagate(False)
    secondary_main_frame.pack()

    # Слева: файлы дистрибьюторов #######################################################################

    input_frame = Frame(secondary_main_frame, width=500, height=500, background="lightgrey")
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


    def edit_dist_file(event):
        global SECONDARY_SELECTED_DIST_FILE_INDEX
        SECONDARY_SELECTED_DIST_FILE_INDEX = input_listbox.curselection()[0]
        selected_dist_file = SECONDARY_INPUT_DIST_FILES[SECONDARY_SELECTED_DIST_FILE_INDEX]
        open_secondary_template_modal(
            root,
            input_listbox,
            open_file_button,
            render_button,
            not_found_names_listbox,
            not_found_regions_listbox,
            SECONDARY_SELECTED_DIST_FILE_INDEX,
            SECONDARY_CURRENT_RENDERED_FILE,
            SECONDARY_INPUT_DIST_FILES,
            title="Редактировать",
            file_txt=str(selected_dist_file.filename).replace("None", ""),
            distributor=str(selected_dist_file.distributor).replace("None", ""),
            sheet_index=str(selected_dist_file.sheet_index).replace("None", ""),
            name_column=str(selected_dist_file.name_column).replace("None", ""),
            region1_column=str(selected_dist_file.region1_column).replace("None", ""),
            region2_column=str(selected_dist_file.region2_column).replace("None", ""),
            sold_number_column=str(selected_dist_file.sold_number_column).replace("None", ""),
            client_column=str(selected_dist_file.client_column).replace("None", ""),
            start_row_number=str(selected_dist_file.start_row_number).replace("None", ""),
            enable_delete_button=True,
            mode="update"
        )

    input_listbox.bind("<Double-1>", edit_dist_file)


    input_listbox_scrollbar.config(command=input_listbox.yview)

    # Кнопка "Добавить" для добавления новых данных
    new_data_edit_button = Button(input_frame, 
                                text="Добавить", 
                                command=lambda:open_secondary_template_modal(
                                    secondary_tab,
                                    input_listbox,
                                    open_file_button,
                                    render_button,
                                    not_found_names_listbox,
                                    not_found_regions_listbox,
                                    SECONDARY_SELECTED_DIST_FILE_INDEX,
                                    SECONDARY_CURRENT_RENDERED_FILE,
                                    SECONDARY_INPUT_DIST_FILES
                                    )
                                )
    new_data_edit_button.pack(pady=10)


    def clear_data():
        global SECONDARY_SELECTED_DIST_FILE_INDEX, SECONDARY_CURRENT_RENDERED_FILE
        input_listbox.delete(0, END)
        not_found_names_listbox.delete(0,END)
        not_found_regions_listbox.delete(0,END)
        SECONDARY_INPUT_DIST_FILES.clear()
        SECONDARY_SELECTED_DIST_FILE_INDEX = None
        SECONDARY_CURRENT_RENDERED_FILE = None
        render_button.config(state="disabled")
        open_file_button.config(state="disabled")

    # Кнопка для очистки списка файлов дистрибьюторов
    clear_input_lisbox_button = Button(input_frame, text="Очистить", command=clear_data)
    clear_input_lisbox_button.place(x=10, y=460)


    # Справа: ненайденные #######################################################################

    not_founds_frame = Frame(secondary_main_frame, width=500, height=500)
    not_founds_frame.pack_propagate(False)
    not_founds_frame.pack()

    # Справа сверху - ненайденные регионы: #######################################################################

    not_found_regions_frame = Frame(not_founds_frame, width=500, height=250, background="lightgrey")
    not_found_regions_frame.pack_propagate(False)
    not_found_regions_frame.pack()

    not_found_regions_title = Label(not_found_regions_frame, text="Ненайденные регионы", background="lightgrey", font=("Arial", 10, "bold"))
    not_found_regions_title.pack(pady=5)

    not_found_regions_listbox_frame = Frame(not_found_regions_frame, width=500, height=210, background="lightgrey")
    not_found_regions_listbox_frame.pack_propagate(False)
    not_found_regions_listbox_frame.pack(anchor='nw')


    not_found_regions_listbox_scrollbar = Scrollbar(not_found_regions_listbox_frame)
    not_found_regions_listbox_scrollbar.pack(side=RIGHT, fill=Y)

    not_found_regions_listbox = Listbox(not_found_regions_listbox_frame, width=78, yscrollcommand=not_found_regions_listbox_scrollbar.set)
    not_found_regions_listbox.pack(side=RIGHT, fill=Y)

    not_found_regions_listbox_scrollbar.config(command=not_found_regions_listbox.yview)


    not_found_regions_listbox.bind(
        "<Double-1>", 
        lambda event: open_insert_modal(event, secondary_tab, open_file_button, "region", not_found_regions_listbox)
    )


    # Справа снизу - ненайденные наименования: #######################################################################

    not_found_names_frame = Frame(not_founds_frame, width=500, height=250, background="lightgrey")
    not_found_names_frame.pack_propagate(False)
    not_found_names_frame.pack()

    not_found_names_title = Label(not_found_names_frame, text="Ненайденные наименования", background="lightgrey", font=("Arial", 10, "bold"))
    not_found_names_title.pack(pady=5)

    not_found_names_listbox_frame = Frame(not_found_names_frame, width=500, height=210, background="lightgrey")
    not_found_names_listbox_frame.pack_propagate(False)
    not_found_names_listbox_frame.pack(anchor='nw')


    not_found_names_listbox_scrollbar = Scrollbar(not_found_names_listbox_frame)
    not_found_names_listbox_scrollbar.pack(side=RIGHT, fill=Y)

    not_found_names_listbox = Listbox(not_found_names_listbox_frame, width=78, yscrollcommand=not_found_names_listbox_scrollbar.set)
    not_found_names_listbox.pack(side=RIGHT, fill=Y)

    not_found_names_listbox_scrollbar.config(command=not_found_names_listbox.yview)


    not_found_names_listbox.bind(
        "<Double-1>", 
        lambda event: open_insert_modal(event, secondary_tab, open_file_button, "name", not_found_names_listbox)
    )


    def render():
        try:
            global SECONDARY_CURRENT_RENDERED_FILE
            now = datetime.now()
            SECONDARY_CURRENT_RENDERED_FILE = f"Reports/Report-{now.strftime("%d%m%Y%H%M%S%f")[:-3]}.xlsx"
            total = TotalReport(*SECONDARY_INPUT_DIST_FILES)
            not_found_names, not_found_regions = total.make_excel(SECONDARY_CURRENT_RENDERED_FILE)

            not_found_names_listbox.delete(0,END)
            for unknown_name in not_found_names:
                not_found_names_listbox.insert(END, unknown_name)

            not_found_regions_listbox.delete(0,END)
            for unknown_region in not_found_regions:
                not_found_regions_listbox.insert(END, unknown_region)
            
            open_file_button.config(state="normal")

        except Exception as err:
            messagebox.showerror(err)
            raise err

    Frame(secondary_tab, height=10).pack()




    render_button = Button(secondary_tab, text="Расчитать", font=('Arial', 12, 'bold'), state="disabled", command=render)
    render_button.pack(pady=0)

    def open_rendered_file():
        os.startfile(os.path.abspath(SECONDARY_CURRENT_RENDERED_FILE))

    open_file_button = Button(secondary_tab, text="Открыть файл", state="disabled", command=open_rendered_file)
    open_file_button.pack(side=RIGHT, anchor='n', padx=20)


    # модальное окно для редактирования БД:

    database_button = Button(secondary_tab, text="База данных", command=lambda:open_database_modal(root))
    database_button.pack(side=LEFT, anchor='n', padx=20)