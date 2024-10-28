non_division_buyers = [
    '"PHARMA COSMOS" MCHJ',
    'MEROS PHARM MChJ',
    'NAVBAHOR APTEKA MCHJ',
    'OOO "TABLETKA-PLYUS"',
    'OOO «PHARMACOSMOS»',
    'OOO TABLETKA-PLYUS',
    'Pharma Choice MCHJ',
    'PHARMA CHOICE MCHJ',
    'PHARMA CHOICE ХК-1',
    'PHARMA COSMOS MChJ',
    'TABLETKA-PLYUS MChJ',
    'YOUNG PHARM MCHJ',
    'ZENTA PHARM MChJ',
    'ЗЕНТА ФАРМ ООО',
    'ИП ООО "ASKLEPIY"',
    'Окси мед',
    'ООО "ASKLEPIY"',
    'ТАБЛЕТКА-ПЛЮС ООО',
    'Ташкент GRAND BEST РЦ',
    'ФАРМА КОСМОС Ч/П (ФАРМ ЛЮКС ИНВЕСТ)'
]

divided_sellings = {
    # На всех
    ('ГАРМОНИЯ ФАРМ КЛИЕНТ', 'ГЕНЕСИС ФАРМА  МЧЖ 100 %',
     'КОИНОТ РТМ Ч/П', '"KOINOT-RADIO TEXNIKA MOLLARI" xususiy korxonasi',
     'ASTOR ALLIANCE MChJ', 'Garmoniya Farm MCHJ', 'GENESIS PHARMA MCHJ',
     'Koinot Radio Texnika Mollar XK', 'MEMORY PHARM A G MCHJ',
     'OOO "GENESIS PHARMA"', 'SALOMATLIK-A MCHJ', 'WHOLE-PHARM MCHJ',
     'YUMAXFARM-SERVIS MChJ'): (1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                11, 12, 13, 14, 15, 16, 17, 18,
                                19, 20, 21, 22, 23, 24),

    # На Ташкент и Таш обл
    ('Anvar Farm Servis XK', 'CITY PHARM MChJ', 'Saidazim Farm Savdo MCHJ',
     'T753', 'T754', 'T755', 'T756', 'ИП ООО  PHARMACLICK',
     'ООО SUPRA LABS', 'СИТЙ ФАРМ МЧЖ'): (1, 2, 3, 4, 5, 6,
                                          7, 8, 9, 10, 11, 12),

    # На Ташкент
    ('7777 ФАРМ МЧЖ', '7777 PHARM MCHJ', '7777-Farm MChJ',
     'IBRAT COMPANY MChJ', 'MCHJ"IBRAT COMPANY"', 'UNIVERSAL-FARM-PLUS MChJ',
     'АББОС МЕДПЕРДСТАВИТЕЛЬ', 'Бахтияр Тургунович', 'Мерум Капитал ЧФ',
     'Расход на филиал', 'Севда ЧА'): (1, 2, 3, 4, 5, 6,
                                       7, 8, 9, 10, 11),

    # На Таш обл
    ('"IFORZODA SHIFO " MCHJ',): (12,),

    # На Самарканд, Термез, Бухара, Хорезм
    ('БЕК БАРАКА', 'ПАРАДИСЕ ФАРМ МЧЖ (ЭЛЕСИУМ ООО КЛИЕНТ)',
     'Biotek Farm MCHJ', 'ORIYO-MEHR MChJ',
     'BEK BARAKA SAMARQAND XK'): (18, 20, 21, 23),

    # На М-Улугбекский, Ю-Абадский, Яккасарайский, Мирабадский районы
    ('SHOHFARM MCHJ',): (3, 4, 8, 9)
}


def get_regions(indices: tuple):
    all_regions = [
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
        'Неизвестный р.'
    ]
    return [all_regions[index] for index in indices]



def divide(client: str, sold_number: int):
    '''
    return: regions(list), sold_number_each(int)
    '''
    global non_division_buyers, divided_sellings
    all_regions = (
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
        'Респ. Каракалпакстан'
    )

    if client in non_division_buyers:
        return all_regions, 0
    else:
        for clients_tuple in divided_sellings:
            if client in clients_tuple:                
                regions_indices = divided_sellings[clients_tuple]
                regions_sold = [all_regions[index-1] for index in regions_indices]
                sold_number_each = round(sold_number / len(regions_indices))
                return regions_sold, sold_number_each
    return None



