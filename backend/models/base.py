from typing import Type

from bson.objectid import ObjectId
from pymotyc import MotycModel
from pydantic import BaseModel, Field, constr


NameStr = constr(max_length=128)


class BaseMongoModel(MotycModel):
    IdType = str
    MongoIdType = ObjectId


class OutModelWithStrId(BaseModel):
    id: str = Field(...)


def instantiate_model(model_type: Type, parameters: tuple):
    assert issubclass(model_type, BaseModel)
    model_fields = model_type.__fields__.keys()
    model_dict = {key: parameters[i] for i, key in enumerate(model_fields)}
    return model_type(**model_dict)
