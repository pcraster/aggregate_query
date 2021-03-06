import os
import tempfile


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("EMIS_AGGREGATE_QUERY_SECRET_KEY") or \
        "yabbadabbadoo!"
    JSON_AS_ASCII = False

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("EMIS_AGGREGATE_QUERY_DEV_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "aggregate_query-dev.sqlite")


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestConfiguration(Configuration):

    # SERVER_NAME = os.environ.get("EMIS_AGGREGATE_QUERY_SERVER_NAME") or \
    #     "localhost"
    # TESTING = True

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("EMIS_AGGREGATE_QUERY_TEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "aggregate_query-test.sqlite")


class ProductionConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("EMIS_AGGREGATE_QUERY_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "aggregate_query.sqlite")


configuration = {
    "development": DevelopmentConfiguration,
    "test": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
