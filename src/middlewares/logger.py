import logging


class LoggerMiddleware:
    def init_logger(self, app):
        app.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] in %(module)s: %(message)s"
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
