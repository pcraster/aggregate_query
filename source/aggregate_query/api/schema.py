import datetime
import uuid
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
            raise ValidationError("Value ({}) must be one of ({})".format(
                data, ", ".join(values)))

    return validator


class AggregateQuerySchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("user", "model", "edit_status", "execute_status",
            "_links")


    id = fields.UUID(dump_only=True)
    user = fields.UUID(required=True)
    model = fields.Str(required=False, missing="")
    edit_status = fields.Str(required=False, missing="draft",
        validate=must_be_one_of(["draft", "final"]))
    execute_status = fields.Str(required=False, missing="pending",
        validate=must_be_one_of(["pending", "queued", "executing", "failed",
            "succeeded"]))
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    _links = ma.Hyperlinks({
            "self": ma.URLFor("api.aggregate_query", user_id="<user>",
                query_id="<id>"),
            "collection": ma.URLFor("api.aggregate_queries", user_id="<user>")
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
            id=uuid.uuid4(),
            user=data["user"],
            model=data["model"],
            edit_status = data["edit_status"],
            execute_status = data["execute_status"],
            posted_at=datetime.datetime.utcnow()
        )
