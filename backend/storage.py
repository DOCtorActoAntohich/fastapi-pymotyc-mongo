from pymongo import IndexModel
from pymotyc import Collection, Engine as PymotycEngine

from backend.models import Weapon, Player


pymotyc_engine = PymotycEngine()


def unique_field_collection(unique_field_name: str) -> Collection:
    return Collection(indexes=[IndexModel(unique_field_name, unique=True)])


@pymotyc_engine.database
class Storage:
    weapons: Collection[Weapon]
    players: Collection[Player] = unique_field_collection("email")
