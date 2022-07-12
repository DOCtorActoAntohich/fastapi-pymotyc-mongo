from pydantic import EmailStr, Field

from backend.models.base import BaseMongoModel, NameStr
from backend.models.weapon import Weapon


class Player(BaseMongoModel):
    IdType = EmailStr

    email: IdType = Field(...)
    name: NameStr = Field(...)
    level: int = Field(1)
    weapons: list[Weapon.IdType] = Field([])
