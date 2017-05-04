import os


class Configuration:

    NC_RABBITMQ_DEFAULT_USER = os.environ.get("NC_RABBITMQ_DEFAULT_USER")
    NC_RABBITMQ_DEFAULT_PASS = os.environ.get("NC_RABBITMQ_DEFAULT_PASS")
    NC_RABBITMQ_DEFAULT_VHOST = os.environ.get("NC_RABBITMQ_DEFAULT_VHOST")


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    pass


class TestConfiguration(Configuration):

    pass


class ProductionConfiguration(Configuration):

    pass


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
