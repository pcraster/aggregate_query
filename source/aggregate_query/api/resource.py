from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import AggregateQueryModel
from .schema import AggregateQuerySchema


aggregate_query_schema = AggregateQuerySchema()


class AggregateQueryResource(Resource):

    def get(self,
            query_id):

        query = AggregateQueryModel.query.get(query_id)

        if query is None:
            raise BadRequest("Aggregate query could not be found")


        data, errors = aggregate_query_schema.dump(query)

        if errors:
            raise InternalServerError(errors)


        return data


class AggregateQueriesResource(Resource):

    def get(self):

        queries = AggregateQueryModel.query.all()
        data, errors = aggregate_query_schema.dump(queries, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        query, errors = aggregate_query_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write query to database.
        db.session.add(query)
        db.session.commit()


        # From record in database to dict representing an aggregate query.
        data, errors = aggregate_query_schema.dump(
            AggregateQueryModel.query.get(query.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data
