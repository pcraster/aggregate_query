from flask import jsonify
from . import api_blueprint


def app_errorhandler(
        exception):
    response = jsonify({
            "status_code": exception.code,
            "message": exception.description,
        })
    return response, exception.code


@api_blueprint.app_errorhandler(400)
def bad_request(exception):
    return app_errorhandler(exception)


@api_blueprint.app_errorhandler(404)
def not_found(exception):
    return app_errorhandler(exception)


@api_blueprint.app_errorhandler(405)
def method_not_allowed(exception):
    return app_errorhandler(exception)


@api_blueprint.app_errorhandler(422)
def unprocessable_entity(exception):
    return app_errorhandler(exception)


@api_blueprint.app_errorhandler(500)
def internal_server_error(exception):
    return app_errorhandler(exception)
