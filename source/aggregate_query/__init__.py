from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .configuration import configuration


db = SQLAlchemy()


def create_app(
        configuration_name):
    app = Flask(__name__)
    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)


    db.init_app(app)


    # Attach routes and custom error pages.
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)


    return app
