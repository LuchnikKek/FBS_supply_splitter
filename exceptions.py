class ApiException(Exception):
    pass


class SuppliesListGettingException(ApiException):
    def __init__(self, request_result):
        self.request_result = request_result
        request_result_text = request_result.text
        super().__init__(
            f'Список поставок не получен.\n'
            f'{request_result_text=}'
        )


class OrderNotAddedException(ApiException):
    def __init__(self, order_id, supply_id, request_result):
        self.order_id = order_id
        self.supply_id = supply_id
        self.request_result = request_result
        request_result_text = request_result.text
        super().__init__(
            f'Заказ {order_id} не добавлен в поставку {supply_id}.\n'
            f'{request_result_text=}'
        )


class SupplyNotCreatedException(ApiException):
    def __init__(self, name, request_result):
        self.name = name
        self.request_result = request_result
        request_result_text = request_result.text
        super().__init__(
            f'Не удалось создать поставку {name}.\n'
            f'{request_result_text=}'
        )