from flask import Flask, jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import atexit
import pydantic
from typing import Optional


DSN = 'postgresql://app:1234@127.0.0.1:5431/netology'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


app = Flask('server')

Base = declarative_base()


class HttpError(Exception):

    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(err: HttpError):
    responce = jsonify({
        'status': 'error',
        'message': err.message
    })
    responce.status_code = err.status_code
    return responce


def on_exit():
    engine.dispose()


atexit.register(on_exit)


Base.metadata.create_all(engine)


class CreateAdSchema(pydantic.BaseModel):
    header: str
    description: str
    owner: str

    @pydantic.validator('header')
    def header_not_epty(cls, value: str):
        if len(value) == 0:
            raise ValueError('header_is_empty')
        return value

    @pydantic.validator('description')
    def description_not_epty(cls, value: str):
        if len(value) == 0:
            raise ValueError('description_is_empty')
        return value

    @pydantic.validator('owner')
    def owner_not_epty(cls, value: str):
        if len(value) == 0:
            raise ValueError('owner_is_empty')
        return value


class PatchAdSchema(pydantic.BaseModel):
    header: Optional[str]
    description: Optional[str]
    owner: Optional[str]

    @pydantic.validator('header')
    def header_not_epty(cls, value: str):
        if len(value) == 0:
            raise ValueError('header_is_empty')
        return value

    @pydantic.validator('description')
    def description_not_epty(cls, value: str):
        if len(value) == 0:
            raise ValueError('description_is_empty')
        return value

    @pydantic.validator('owner')
    def owner_not_epty(cls, value: str):
        if len(value) == 0:
            raise ValueError('owner_is_empty')
        return value


if __name__ == "__main__":
    app.run()
