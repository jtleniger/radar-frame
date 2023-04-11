from configparser import ConfigParser

class Config:
    _config = None

    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read('./config/config.ini')

    def __getitem__(self, key):
        return self._parser.__getitem__(key)

    @staticmethod
    def instance():
        if Config._config is None:
            Config._config = Config()

        return Config._config