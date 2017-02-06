import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from marshmallow.validate import Length, OneOf
from .. import ma
from .model import *


class AggregateQuerySchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("id", "user", "model", "edit_status", "execute_status",
            "posted_at", "patched_at", "_links")


    id = fields.UUID(dump_only=True)
    user = fields.UUID(required=True)
    model = fields.Dict(required=True)
    edit_status = fields.Str(required=False, missing="draft",
        validate=OneOf(["draft", "final"]))
    execute_status = fields.Str(required=False, missing="pending",
        validate=OneOf(["pending", "queued", "executing", "failed",
            "succeeded"]))
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    patched_at = fields.DateTime(dump_only=True,
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
            posted_at=datetime.datetime.utcnow(),
            patched_at=datetime.datetime.utcnow(),
        )


class AggregateQueryResultSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("id", "uri", "_links")


    id = fields.UUID(required=True)
    uri = fields.Str(required=True, validate=Length(min=1))
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    _links = ma.Hyperlinks({
            "self": ma.URLFor("api.aggregate_query_result", query_id="<id>"),
            "collection": ma.URLFor("api.aggregate_query_results")
        })


    def key(self,
            many):
        return "aggregate_query_results" if many else "aggregate_query_result"


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
        return AggregateQueryResultModel(
            id=data["id"],
            uri=data["uri"],
            posted_at=datetime.datetime.utcnow()
        )


class AggregateQueryMessageSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("id", "message", "_links")


    id = fields.UUID(required=True)
    message = fields.Str(required=True, validate=Length(min=1))
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    _links = ma.Hyperlinks({
            "self": ma.URLFor("api.aggregate_query_message", query_id="<id>"),
            "collection": ma.URLFor("api.aggregate_query_messages")
        })


    def key(self,
            many):
        return "aggregate_query_messages" if many else "aggregate_query_message"


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
        return AggregateQueryMessageModel(
            id=data["id"],
            message=data["message"],
            posted_at=datetime.datetime.utcnow()
        )
