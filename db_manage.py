import sqlite3
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

db_con = sqlite3.connect('reports.db')
db_con.row_factory = sqlite3.Row
cursor = db_con.cursor()


def get_general_name(unique_name):
    # while unique_name[-1] == ' ':
    #     unique_name = unique_name[:-1]
    
    cursor.execute(
        f"""SELECT name 
        FROM General_Names INNER JOIN All_names 
        ON General_Names.id = All_names.general_id 
        WHERE unique_name = '{unique_name.strip()}'"""
    )

    result = cursor.fetchone()
    db_con.commit()
    return result[0] if result is not None else None


def get_group_of_gen_name(general_name):
    cursor.execute(
        f"""SELECT "group" FROM Groups
        INNER JOIN General_Names 
        ON Groups.group_id=General_Names.group_id 
        WHERE General_Names.name='{general_name.strip()}'"""
    )

    result = cursor.fetchone()
    db_con.commit()
    return result[0] if result is not None else None


def get_general_region(unique_region: str):
    try:
        unique_region = unique_region.replace('\n', '')
    except AttributeError:
        pass

    if unique_region == 0:
        return None

    try:
        unique_region = unique_region.replace('\t', '')
    except AttributeError:
        pass

    try:
        unique_region = unique_region.strip()
    except:
        pass


    # unique_region = unique_region.replace("'", "\'")

    cursor.execute(
        f"""SELECT region 
        FROM General_Regions INNER JOIN All_Regions 
        ON General_Regions.id = All_Regions.general_id 
        WHERE unique_region = (?)""",
        (unique_region,)
    )

    result = cursor.fetchone()
    db_con.commit()
    return result[0] if result is not None else None


def get_general_region_by_id(region_id):
    cursor.execute(
        f"""SELECT region 
        FROM General_Regions
        WHERE id = {region_id}"""
    )

    result = cursor.fetchone()
    db_con.commit()

    return result['region'] if result is not None else None


def get_all_names(sort_by_group=True, include_regions=True):
    regions = [
        'Total',
        'Алмазарский р. (Ташкент)',
        'Бектемирский р. (Ташкент)',
        'Мирабадский р. (Ташкент)',
        'М.Улугбекский р. (Ташкент)',
        'Сергелийский р. (Ташкент)',
        'Чиланзарский р. (Ташкент)',
        'Шайхантахурский р. (Ташкент)',
        'Юнусабадский р. (Ташкент)',
        'Яккасарайский р. (Ташкент)',
        'Яшнабадский р. (Ташкент)',
        'Учтепинский р. (Ташкент)',
        'Ташкентская обл.',
        'Андижанская обл.',
        'Наманганская обл.',
        'Ферганская обл.',
        'Сырдарьинская обл.',
        'Джизакская обл.',
        'Самаркандская обл.',
        'Кашкадарьинская обл.',
        'Сурхандарьинская обл.',
        'Бухарская обл.',
        'Навоинская обл.',
        'Хорезмская обл.',
        'Респ. Каракалпакстан',
        'Неизвестный регион'
    ]

    result = {}

    if sort_by_group:
        """
        result = {
                    "C&P": {
                                "Альфа нормикс": {
                                                    "Total": xxx,
                                                    "Алмазарский район (Ташкент)": ххх,
                                                    "Бектемирский район (Ташкент)": ххх,
                                                    ...
                                                },
                                "Алфавит": {
                                                    "Total": xxx,
                                                    "Алмазарский район (Ташкент)": ххх,
                                                    "Бектемирский район (Ташкент)": ххх,
                                                    ...
                                                },
                                ...
                                },
                    "OTC": {
                                "Альфа нормикс": {
                                                    "Total": xxx,
                                                    "Алмазарский район (Ташкент)": ххх,
                                                    "Бектемирский район (Ташкент)": ххх,
                                                    ...
                                                },
                                "Алфавит": {
                                                    "Total": xxx,
                                                    "Алмазарский район (Ташкент)": ххх,
                                                    "Бектемирский район (Ташкент)": ххх,
                                                    ...
                                                },
                                ...
                                },
                    ...
                }
        
        """
        cursor.execute(
            """SELECT * 
            FROM Groups"""
        )

        groups = cursor.fetchall()
        for group in groups:
            result[group['group']] = {}
            cursor.execute(
                f"""SELECT name 
                FROM General_Names 
                WHERE group_id={group['group_id']}"""
            )
            names_in_group = cursor.fetchall()
            db_con.commit()
            names_sorted = sorted([name['name'] for name in names_in_group])
            for name in names_sorted:
                if name not in result[group['group']]:
                    result[group['group']][name] = {}
                if include_regions:
                    for region in regions:
                        result[group['group']][name][region] = 0
                else:
                    result[group['group']][name]["balance_beginning"] = 0
                    result[group['group']][name]["incomes"] = 0
                    result[group['group']][name]["sold_number"] = 0
                    result[group['group']][name]["balance_end"] = 0

    else:
        cursor.execute(
            f"""SELECT name 
            FROM General_Names"""
        )
        names_unsorted = cursor.fetchall()
        names_sorted = sorted([name['name'] for name in names_unsorted])
        for name in names_sorted:
            result[name] = {}
            if include_regions:
                for region in regions:
                    result[name][region] = 0
            else:
                result[name]["balance_beginning"] = 0
                result[name]["incomes"] = 0
                result[name]["sold_number"] = 0
                result[name]["balance_end"] = 0
        db_con.commit()
    return result


def get_all_regions():
    cursor.execute("SELECT region FROM General_Regions")
    results = cursor.fetchall()
    db_con.commit()
    return [result['region'] for result in results]


def insert_unique_name(unique_name, gen_name):
    cursor.execute(f"""SELECT id FROM General_Names WHERE name='{gen_name.strip()}'""")
    id = cursor.fetchone()[0]

    cursor.execute(f"""
    INSERT INTO All_Names (unique_name, general_id)
    VALUES (?, ?)
    """, (unique_name.strip(), id))
    db_con.commit()


def insert_unique_region(unique_reg, gen_reg):

    # while unique_reg[-1] == ' ':
    #         unique_reg = unique_reg[:-1]
    # while unique_reg[0] == ' ':
    #     unique_reg = unique_reg[1:]
    
    cursor.execute(f"""SELECT id FROM General_Regions WHERE region='{gen_reg.strip()}'""")
    id = cursor.fetchone()[0]

    cursor.execute(f"""
    INSERT INTO All_Regions (unique_region, general_id)
    VALUES (?, ?)
    """, (unique_reg.strip(), id))
    db_con.commit()


def get_groups():
    cursor.execute("""SELECT [group] FROM Groups""")
    groups = cursor.fetchall()
    db_con.commit()
    return [group['group'] for group in groups]


def get_names_data():
    cursor.execute(
        """
            SELECT 
                General_Names.name, 
                Producers.producer, 
                Groups."group", 
                General_Names.price
            FROM 
                General_Names
            JOIN 
                Groups ON General_Names.group_id = Groups.group_id
            JOIN 
                Producers ON General_Names.producer_id = Producers.id;
        """
    )
    result = cursor.fetchall()
    db_con.commit()
    return [[r['name'], r['producer'], r['group'], r['price']] for r in result]


def get_all_producers():
    cursor.execute("SELECT producer FROM Producers")
    results = cursor.fetchall()
    db_con.commit()
    return [result['producer'] for result in results]


def insert_new_general_name(
        name,
        price,
        group,
        producer        
):
    query = """
        INSERT INTO General_Names (name, price, group_id, producer_id)
        VALUES (
            ?, 
            ?, 
            (SELECT group_id FROM Groups WHERE "group" = ?),
            (SELECT id FROM Producers WHERE producer = ?)
        );
    """
    cursor.execute(query, (name, price, group, producer))
    db_con.commit()


def delete_general_name(name):
    cursor.execute(
        f"""
            DELETE FROM General_Names WHERE name='{name}';
        """
    )
    db_con.commit()


def update_general_name(original_name, name, producer, group, price):
    query = """
        UPDATE General_Names
        SET name = ?, 
            producer_id = (SELECT id FROM Producers WHERE producer = ?),
            group_id = (SELECT group_id FROM Groups WHERE "group" = ?),
            price = ?
        WHERE name = ?;
    """
    cursor.execute(query, (name, producer, group, price, original_name))
    db_con.commit()

# print(get_all_producers())

# print(get_all_names()['OTC']['Алфавит Мамино здоровье табл.  №60'].keys())


