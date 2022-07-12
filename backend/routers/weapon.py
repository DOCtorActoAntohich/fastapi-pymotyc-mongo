from fastapi import APIRouter

from backend.models.base import NameStr, instantiate_model
from backend.storage import Storage
from backend.models import WeaponRarity, WeaponIn, Weapon, WeaponOut


weapon_router = APIRouter(prefix="/weapon")


@weapon_router.post("/new/", response_model=WeaponOut)
async def create_new_weapon(name: NameStr, damage: int, cost: int, rarity: WeaponRarity):
    weapon_in = instantiate_model(WeaponIn, (name, damage, cost, rarity))
    weapon = Weapon.from_weapon_in(weapon_in)
    created_weapon = await Storage.weapons.save(weapon, inject_default_id=True)
    return WeaponOut.from_weapon(created_weapon)


@weapon_router.get("/get/{weapon_id}", response_model=WeaponOut)
async def get_weapon_by_id(weapon_id: str) -> WeaponOut:
    weapon = await Storage.weapons.find_one(_id=weapon_id)
    return WeaponOut.from_weapon(weapon)


@weapon_router.get("/all/")
async def list_all_weapons() -> list[WeaponOut]:
    all_weapons = await Storage.weapons.find({})
    return [WeaponOut.from_weapon(weapon) for weapon in all_weapons]


@weapon_router.put("/update/{weapon_id}")
async def update_weapon(weapon_id: str, new_weapon: WeaponIn) -> WeaponOut:
    weapon = Weapon.from_weapon_in(new_weapon, _id=weapon_id)
    updated_weapon = await Storage.weapons.save(item=weapon, mode="update")
    return WeaponOut.from_weapon(updated_weapon)


@weapon_router.delete("/delete/{weapon_id}", status_code=204)
async def delete_weapon(weapon_id: str):
    await Storage.weapons.delete_one(_id=weapon_id)
