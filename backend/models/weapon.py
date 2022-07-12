from enum import auto

from bson.objectid import ObjectId
from pydantic import Field, parse_obj_as, parse_raw_as
from pymotyc import WithId
from fastapi_utils.enums import StrEnum

from backend.models.base import BaseMongoModel, NameStr, OutModelWithStrId


# noinspection PyArgumentList
class WeaponRarity(StrEnum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()
    UNIQUE = auto()


class WeaponIn(BaseMongoModel):
    name: NameStr = Field(...)
    damage: int = Field(...)
    cost: int = Field(...)
    rarity: WeaponRarity = Field(...)


class Weapon(WeaponIn, WithId):
    @classmethod
    def from_weapon_in(cls, item_in: WeaponIn, *, _id: str = None):
        weapon = parse_obj_as(cls, item_in)
        if _id is not None:
            weapon.id = ObjectId(_id)
        return weapon


class WeaponOut(WeaponIn, OutModelWithStrId):
    @classmethod
    def from_weapon(cls, item: Weapon):
        return parse_raw_as(cls, item.json())
