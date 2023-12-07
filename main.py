import os
from typing import Dict

import requests
from dotenv import load_dotenv

from constants import WB_FBS_URLS
from constants import logger
from exceptions import (
    OrderNotAddedException,
    SupplyNotCreatedException,
    SuppliesListGettingException,
    OrdersListGettingException
)
from models import Order, Supply


class WB_Interface:
    def __init__(self, token):
        self.token: str = token
        self.supplies: list[Supply] = []
        self.orders: list[Order] = []

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
            logger.info('Список поставок получен.')
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
            logger.info('Поставка {} создана успешно.'.format(name))
            return result.json()['id']

    def get_new_orders(self) -> list[Dict]:
        result = requests.get(
            url=WB_FBS_URLS.NEW_ORDERS_URL,
            headers={'Authorization': self.token},
        )
        if not result.status_code == 200:
            logger.error('Ошибка при получении списка заказов.')
            raise OrdersListGettingException(result)
        else:
            orders = result.json()['orders']
            logger.info('Список заказов получен.')
            logger.info('Новых заказов: {}.'.format(len(orders)))
            return orders

    def add_order_to_supply(self, supply_id, order_id, log_number: int = None) -> None:
        result = requests.patch(
            url=WB_FBS_URLS.SUPPLY_ADD_ORDER.format(supply_id, order_id),
            headers={'Authorization': self.token},
        )
        if not result.status_code == 204:
            logger.error('Ошибка при добавлении заказа в поставку.')
            raise OrderNotAddedException(order_id, supply_id, result)
        else:
            logger.info(f'Заказ{" #" + str(log_number) if log_number else None} добавлен в поставку.')

    def split_orders_by_supplies(self) -> None:
        self.supplies = self.get_supplies()
        self.orders = [Order(**order) for order in self.get_new_orders()]
        supplies_ids_by_names: Dict[str, str] = {supply.name: supply.id for supply in self.supplies}

        for log_number, order in enumerate(self.orders, start=1):
            supply_name = order.article

            if (supply_id := supplies_ids_by_names.get(supply_name)) is None:
                logger.info('Поставка {} не найдена.'.format(supply_name))
                supply_id = self.create_supply(supply_name)
                self.supplies.append(
                    Supply(
                        id=supply_id,
                        done=False,
                        createdAt='создана на клиенте, уточнить',
                        closedAt=None,
                        scanDt=None,
                        name=supply_name,
                        cargoType=1
                    )
                )
                supplies_ids_by_names[supply_name] = supply_id
            self.add_order_to_supply(supply_id=supply_id, order_id=order.id, log_number=log_number)
        logger.info('Все заказы распределены по поставкам.')


if __name__ == '__main__':
    load_dotenv()
    wb_i = WB_Interface(os.environ.get('TOKEN'))
    wb_i.split_orders_by_supplies()
