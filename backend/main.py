import bson.errors
import pymongo.errors
import pymotyc
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from backend.settings import Settings
from backend.storage import Storage, pymotyc_engine

from backend.routers import player_router, weapon_router


app = FastAPI()


async def connect_to_database():
    mongo_client = AsyncIOMotorClient(Settings.mongo.connection_url)
    await pymotyc_engine.bind(
        motor=mongo_client,
        inject_motyc_fields=True
    )
    await Storage.players.create_indexes()


def include_routers():
    app.include_router(player_router)
    app.include_router(weapon_router)


@app.on_event("startup")
async def on_backend_startup():
    await connect_to_database()
    include_routers()


@app.exception_handler(pymotyc.errors.NotFound)
async def on_key_not_found_error(_request, exc):
    return JSONResponse({"detail": str(exc)}, status_code=404)


@app.exception_handler(pymongo.errors.DuplicateKeyError)
async def on_duplicate_key_error(_request, exc):
    return JSONResponse({"detail": str(exc)}, status_code=400)


@app.exception_handler(bson.errors.InvalidId)
async def on_invalid_id_error(_request, exc):
    return JSONResponse({"detail": str(exc)}, status_code=400)


@app.get("/")
async def read_root():
    return "Welcome to City 17!"
