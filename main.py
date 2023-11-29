from models import Order, Supply
from constants import WB_FBS_URLS, ARTICLE_TO_SUPPLY_NAME
import requests
from typing import Dict
import os


class WB_Interface:
    def __init__(self, token):
        self.token = token

    def get_supplies(self) -> list[Supply]:
        result = requests.get(
            url=WB_FBS_URLS.SUPPLIES_LIST_URL,
            params={'limit': 1000, 'next': 0},
            headers={'Authorization': self.token},
        ).json()
        return [Supply(**supply) for supply in result['supplies'] if not supply['done']]

    def get_new_orders(self) -> list[Dict]:
        result = requests.get(
            url=WB_FBS_URLS.NEW_ORDERS_URL,
            headers={'Authorization': self.token},
        ).json()
        return result['orders']

    def add_order_to_supply(self, supply_id, order_id) -> bool:
        result = requests.patch(
            url=WB_FBS_URLS.SUPPLY_ADD_ORDER.format(supply_id, order_id),
            headers={'Authorization': self.token},
        )
        return result.status_code == 204


if __name__ == '__main__':
    wb_i = WB_Interface(os.getenv('TOKEN'))

    const_supplies_names = ARTICLE_TO_SUPPLY_NAME.values()
    current_supplies: list[Supply] = wb_i.get_supplies()

    # check if supplies are created
    for supply_name in const_supplies_names:
        if supply_name not in map(lambda x: x.name, current_supplies):
            raise Exception('Поставка {} не создана'.format(supply_name))

    current_supplies_ids_map: Dict[str, str] = {
        supply.name: supply.id
        for supply in current_supplies
        if supply.name in const_supplies_names
    }

    orders: list[Order] = [Order(**order) for order in wb_i.get_new_orders()]

    for order in orders:
        wb_i.add_order_to_supply(
            order_id=order.id,
            supply_id=current_supplies_ids_map[ARTICLE_TO_SUPPLY_NAME[order['article']]]
        )
