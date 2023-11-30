import logging

from typing import Dict


class WB_FBS_URLS:
    NEW_ORDERS_URL = 'https://suppliers-api.wildberries.ru/api/v3/orders/new'
    SUPPLIES_LIST_URL = 'https://suppliers-api.wildberries.ru/api/v3/supplies'
    SUPPLY_ADD_ORDER = 'https://suppliers-api.wildberries.ru/api/v3/supplies/{}/orders/{}'
    CREATE_SUPPLY_URL = 'https://suppliers-api.wildberries.ru/api/v3/supplies'


# Артикул поставщика: Название поставки
ARTICLE_TO_SUPPLY_NAME: Dict[str, str] = {
    'Зеленый_Налобный_Датчик_Движения': 'зеленый с датчиком',
    'PM10-TG': 'ручной пм10тг',
    'A850': 'А850',
    '2261_ЧерныйОдноцветный': 'черный одноцветный',
    'RED_PM10_DRAGON': 'ручной DRAGON',
}

file_handler = logging.FileHandler(filename='logs.log')
console_handler = logging.StreamHandler()
logging.basicConfig(handlers=(file_handler, console_handler),
                    level=logging.INFO,
                    format="[%(asctime)s | %(levelname)s]: %(message)s",
                    datefmt='%d.%m.%Y %H:%M:%S')
logger = logging.getLogger(__name__)
