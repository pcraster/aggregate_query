from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import *
from .schema import *


aggregate_query_schema = AggregateQuerySchema()


class AggregateQueryResource(Resource):

    def get(self,
            user_id,
            query_id):

        # user_id is not needed
        query = AggregateQueryModel.query.get(query_id)

        if query is None or query.user != user_id:
            raise BadRequest("Aggregate query could not be found")


        data, errors = aggregate_query_schema.dump(query)

        if errors:
            raise InternalServerError(errors)


        return data

    def patch(self,
            user_id,
            query_id):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # user_id is not needed
        query = AggregateQueryModel.query.get(query_id)

        if query is None or query.user != user_id:
            raise BadRequest("Aggregate query could not be found")


        # Merge current representation and the edits passed in.
        for field_name in json_data:
            if hasattr(query, field_name):
                setattr(query, field_name, json_data[field_name])

        db.session.commit()


        data, errors = aggregate_query_schema.dump(query)

        if errors:
            raise InternalServerError(errors)


        return data


    def delete(self,
            user_id,
            query_id):

        # user_id is not needed
        query = AggregateQueryModel.query.get(query_id)

        if query is None or query.user != user_id:
            raise BadRequest("Aggregate query could not be found")


        # Delete query from database.
        db.session.delete(query)
        db.session.commit()


        data, errors = aggregate_query_schema.dump(query)

        if errors:
            raise InternalServerError(errors)


        return data


class AggregateQueriesResource(Resource):

    def get(self,
            user_id):

        queries = AggregateQueryModel.query.filter_by(user=user_id)
        data, errors = aggregate_query_schema.dump(queries, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


class AggregateQueriesAllResource(Resource):


    # TODO Only call this from admin interface!
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


        return data, 201


aggregate_query_result_schema = AggregateQueryResultSchema()


class AggregateQueryResultResource(Resource):

    def get(self,
            query_id):

        result = AggregateQueryResultModel.query.get(query_id)

        if result is None:
            raise BadRequest("Aggregate query result could not be found")


        data, errors = aggregate_query_result_schema.dump(result)

        if errors:
            raise InternalServerError(errors)


        return data


class AggregateQueryResultsResource(Resource):

    def get(self):

        results = AggregateQueryResultModel.query.all()
        data, errors = aggregate_query_result_schema.dump(results, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        result, errors = aggregate_query_result_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write result to database.
        db.session.add(result)
        db.session.commit()


        # From record in database to dict representing an aggregate query.
        data, errors = aggregate_query_result_schema.dump(
            AggregateQueryResultModel.query.get(result.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201


aggregate_query_message_schema = AggregateQueryMessageSchema()


class AggregateQueryMessageResource(Resource):

    def get(self,
            query_id):

        message = AggregateQueryMessageModel.query.get(query_id)

        if message is None:
            raise BadRequest("Aggregate query message could not be found")


        data, errors = aggregate_query_message_schema.dump(message)

        if errors:
            raise InternalServerError(errors)


        return data


class AggregateQueryMessagesResource(Resource):

    def get(self):

        messages = AggregateQueryMessageModel.query.all()
        data, errors = aggregate_query_message_schema.dump(messages, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        message, errors = aggregate_query_message_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write message to database.
        db.session.add(message)
        db.session.commit()


        # From record in database to dict representing an aggregate query.
        data, errors = aggregate_query_message_schema.dump(
            AggregateQueryMessageModel.query.get(message.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201
