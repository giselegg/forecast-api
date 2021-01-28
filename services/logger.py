from logging import getLogger, FileHandler, Formatter, INFO


class LogDecorator:
    @staticmethod
    def log_singleton(log_cls):
        class_instances = {}

        def get_instance(*args, **kwargs):
            key = (log_cls, args, str(kwargs))
            if key not in class_instances:
                class_instances[key] = log_cls(*args, **kwargs)
            return class_instances[key]

        return get_instance


@LogDecorator.log_singleton
class RequestLogger():
    def __init__(self, name, logfile):
        self.logger = getLogger(name)
        self.logger.setLevel(INFO)
        formatter = Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = FileHandler(logfile)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
