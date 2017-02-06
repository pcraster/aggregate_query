from sqlalchemy_utils import JSONType, UUIDType
from .. import db


class AggregateQueryModel(db.Model):
    id = db.Column(UUIDType(), primary_key=True)
    user = db.Column(UUIDType())
    model = db.Column(JSONType)
    edit_status = db.Column(db.Unicode(40))
    execute_status = db.Column(db.Unicode(40))
    posted_at = db.Column(db.DateTime)
    patched_at = db.Column(db.DateTime)


class AggregateQueryResultModel(db.Model):
    id = db.Column(UUIDType(), primary_key=True)
    uri = db.Column(db.UnicodeText)
    posted_at = db.Column(db.DateTime)


class AggregateQueryMessageModel(db.Model):
    id = db.Column(UUIDType(), primary_key=True)
    message = db.Column(db.UnicodeText)
    posted_at = db.Column(db.DateTime)
