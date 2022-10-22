from flask.views import MethodView
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
import pydantic


from app.server import Session, HttpError, CreateAdSchema, PatchAdSchema
from app.admodel import Ad


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
        return jsonify({'header': ad.header, 'description': ad.description, 'date': ad.creation_date.isoformat(),
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
