import datetime
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from .. import ma
from .model import AggregateQueryModel


def must_not_be_blank(
        data):
    if not data:
        raise ValidationError("Data not provided")


def must_be_one_of(
        values):

    def validator(
            data):
        if not data in values:
            raise ValidationError("Value must be one of {}".format(" ".join(
                values)))

    return validator


class AggregateQuerySchema(ma.Schema):

    class Meta:
        fields = ("model", "status", "_links")

    id = fields.Int(dump_only=True)
    model = fields.Str(required=False, missing="")
    status = fields.Str(required=False, missing="draft",
        validate=must_be_one_of(["draft", "finished"]))
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    _links = ma.Hyperlinks({
            "self": ma.URLFor("api.aggregate_query", id="<id>"),
            "collection": ma.URLFor("api.aggregate_queries")
        })


    def key(self,
            many):
        return "aggregate_queries" if many else "aggregate_query"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError("Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data, many):
        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):
        return AggregateQueryModel(
            model=data["model"],
            status = data["status"],
            posted_at=datetime.datetime.utcnow()
        )
