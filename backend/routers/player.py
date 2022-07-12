from fastapi import APIRouter
from pydantic import EmailStr

from backend.models.player import Player
from backend.storage import Storage


player_router = APIRouter(prefix="/player")


@player_router.post("/new/", response_model=Player)
async def create_new_player(player: Player) -> Player:
    return await Storage.players.save(player)


@player_router.get("/all/")
async def list_all_players() -> list[Player]:
    return await Storage.players.find({})


@player_router.get("/get/{email}", response_model=Player)
async def get_player_by_email(email: EmailStr) -> Player:
    return await Storage.players.find_one({Player.email: email})


@player_router.delete("/delete/{email}", status_code=204)
async def delete_player_by_email(email: EmailStr):
    await Storage.players.delete_one({Player.email: email})


@player_router.patch("/{email}/level_up", response_model=Player)
async def level_up_player(email: EmailStr) -> Player:
    return await Storage.players.update_one(
        {Player.email: email},
        update={"$inc": {Player.level: 1}}
    )


@player_router.patch("/{email}}/add_weapon", response_model=Player)
async def add_weapon(email: EmailStr, weapon_id: str) -> Player:
    await Storage.weapons.find_one(_id=weapon_id)

    return await Storage.players.update_one(
        {Player.email: email},
        update={"$push": {Player.weapons: weapon_id}}
    )
