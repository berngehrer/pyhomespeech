import logging
import appsettings

class AppLogger:

    def __init__(self, name, file = appsettings.LOG_PATH, lvl = logging.DEBUG):

        ch = logging.StreamHandler()
        ch.setLevel(lvl)
        formatter = logging.Formatter(appsettings.LOG_FORMAT)
        ch.setFormatter(formatter)

        self._logger = logging.getLogger(name)
        self._logger.setLevel(lvl)
        self._logger.addHandler(ch)

        logging.basicConfig(filename=file, level=lvl)   
    

    @property
    def instance(self):
        return self._logger

