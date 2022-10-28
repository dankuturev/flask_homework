from sqlalchemy.exc import IntegrityError
from flask.views import MethodView
from flask import request, jsonify
from typing import Optional
import pydantic
from admodel import Ad
from server import Session, app


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


def validate(Schema, data: dict):
    try:
        data_validated = Schema(**data).dict(exclude_none=True)
    except pydantic.ValidationError as er:
        raise HttpError(400, er.errors())
    return data_validated


def get_ad(ad_id: int, session: Session) -> Ad:
    ad = session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, 'ad_not_found')
    return ad


class AdViews(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
        return jsonify({'header': ad.header, 'description': ad.description, 'date': ad.create_date.isoformat(),
                        'owner': ad.owner})

    def post(self):
        json_data_validated = validate(CreateAdSchema, request.json)
        with Session() as session:
            new_ad = Ad(header=json_data_validated['header'], description=json_data_validated['description'],
                        owner=json_data_validated['owner'])
            try:
                session.add(new_ad)
                session.commit()
            except IntegrityError:
                raise HttpError(400, 'user already exists')
            return jsonify({'status': 'success', 'id': new_ad.id})

    def patch(self, ad_id):
        json_data_validated = validate(PatchAdSchema, request.json)
        with Session() as session:
            ad = get_ad(ad_id, session)
            for key, value in json_data_validated.items():
                setattr(ad, key, value)
                session.add(ad)
                session.commit()
        return jsonify({'status': 'success'})

    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
        return jsonify({'status': 'success'})