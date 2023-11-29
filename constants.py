from typing import Dict


class WB_FBS_URLS:
    NEW_ORDERS_URL = 'https://suppliers-api.wildberries.ru/api/v3/orders/new'
    SUPPLIES_LIST_URL = 'https://suppliers-api.wildberries.ru/api/v3/supplies'
    SUPPLY_ADD_ORDER = 'https://suppliers-api.wildberries.ru/api/v3/supplies/{}/orders/{}'


# Артикул поставщика: Название поставки
ARTICLE_TO_SUPPLY_NAME: Dict[str, str] = {
    'Зеленый_Налобный_Датчик_Движения': 'зеленый с датчиком',
    'PM10-TG': 'ручной пм10тг',
    'A850': 'А850',
    '2261_ЧерныйОдноцветный': 'черный одноцветный',
    'RED_PM10_DRAGON': 'ручной DRAGON',
}
