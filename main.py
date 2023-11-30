import os
from typing import Dict

import requests
from dotenv import load_dotenv

from constants import WB_FBS_URLS, ARTICLE_TO_SUPPLY_NAME
from constants import logger
from exceptions import (
    OrderNotAddedException,
    SupplyNotCreatedException,
    SuppliesListGettingException
)
from models import Order, Supply


class WB_Interface:
    def __init__(self, token):
        self.token = token

    def get_supplies(self) -> list[Supply]:
        result = requests.get(
            url=WB_FBS_URLS.SUPPLIES_LIST_URL,
            params={'limit': 1000, 'next': 0},
            headers={'Authorization': self.token},
        )
        if not result.status_code == 200:
            logger.error('Ошибка при получении списка поставок.')
            raise SuppliesListGettingException(result)
        else:
            return [Supply(**supply) for supply in result.json()['supplies'] if not supply['done']]

    def create_supply(self, name) -> str:
        result = requests.post(
            url=WB_FBS_URLS.CREATE_SUPPLY_URL,
            json={'name': name},
            headers={'Authorization': self.token},
        )
        if not result.status_code == 201:
            logger.error('Ошибка при создании поставки.')
            raise SupplyNotCreatedException(name, result)
        else:
            return result.json()['id']

    def get_new_orders(self) -> list[Dict]:
        result = requests.get(
            url=WB_FBS_URLS.NEW_ORDERS_URL,
            headers={'Authorization': self.token},
        ).json()
        return result['orders']

    def add_order_to_supply(self, supply_id, order_id) -> None:
        result = requests.patch(
            url=WB_FBS_URLS.SUPPLY_ADD_ORDER.format(supply_id, order_id),
            headers={'Authorization': self.token},
        )
        if not result.status_code == 204:
            logger.error('Ошибка при добавлении заказа в поставку.')
            raise OrderNotAddedException(order_id, supply_id, result)


if __name__ == '__main__':
    load_dotenv()
    wb_i = WB_Interface(os.environ.get('TOKEN'))

    const_supplies_names = ARTICLE_TO_SUPPLY_NAME.values()
    wb_supplies: list[Supply] = wb_i.get_supplies()

    # check if all supplies are created
    for supply_name in const_supplies_names:
        if supply_name not in map(lambda x: x.name, wb_supplies):
            logger.info('Поставка {} не создана. Создаю.'.format(supply_name))
            new_supply_id = wb_i.create_supply(supply_name)
            wb_supplies.append(
                Supply(
                    id=new_supply_id,
                    done=False,
                    createdAt='создана на клиенте, уточнить',
                    closedAt=None,
                    scanDt=None,
                    name=supply_name,
                    cargoType=1
                )
            )
            logger.info('Поставка успешно создана.')

    wb_supplies_ids_map: Dict[str, str] = {
        supply.name: supply.id
        for supply in wb_supplies
        if supply.name in const_supplies_names
    }

    orders: list[Order] = [Order(**order) for order in wb_i.get_new_orders()]

    for number, order in enumerate(orders, start=1):
        order_supply_name = ARTICLE_TO_SUPPLY_NAME[order.article]
        wb_i.add_order_to_supply(
            order_id=order.id,
            supply_id=wb_supplies_ids_map[order_supply_name]
        )
        logger.info(f'Заказ #{number} добавлен в поставку.')
    logger.info('Все заказы распределены по поставкам.')
