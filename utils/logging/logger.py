import logging


class LoggerControl:

    def __init__(self, name):
        self._log = logging.getLogger(name)

    def set_level(self, level):
        # create console handler
        ch = logging.StreamHandler() #sys.stdout
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self._log.addHandler(ch)
        self._log.setLevel(level)

    def get_logger(self):
        return self._log


logger_ctl = LoggerControl("blog")
logger_ctl.set_level(logging.INFO)
logger = logger_ctl.get_logger()

