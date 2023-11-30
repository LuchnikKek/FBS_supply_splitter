from typing import List

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Order(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id: int
    rid: str
    created_at: str
    warehouse_id: int
    offices: List[str] | None
    address: None
    user: None
    skus: List[str]
    price: int
    converted_price: int
    currency_code: int
    converted_currency_code: int
    order_uid: str
    delivery_type: str
    nm_id: int
    chrt_id: int
    article: str
    cargo_type: int


class Supply(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id: str
    done: bool
    created_at: str
    closed_at: str | None
    scan_dt: str | None
    name: str
    cargo_type: int
