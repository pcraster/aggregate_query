from .. import db


class AggregateQueryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.UnicodeText)
    status = db.Column(db.Unicode(40))
    posted_at = db.Column(db.DateTime)
