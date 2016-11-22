from sqlalchemy_utils import UUIDType
from .. import db


class AggregateQueryModel(db.Model):
    id = db.Column(UUIDType(), primary_key=True)
    user = db.Column(UUIDType())
    model = db.Column(db.UnicodeText)
    status = db.Column(db.Unicode(40))
    posted_at = db.Column(db.DateTime)
