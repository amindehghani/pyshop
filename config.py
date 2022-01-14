import configparser
import os
import logging
import coloredlogs

_logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=_logger, fmt="%(levelname)s -> %(message)s")


class ConfigParser:
    @staticmethod
    def get_config(section, items):
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
            result_dict = {}
            for item in items:
                result_dict.update({
                    item: config[section][item]
                })
            return result_dict
        except Exception as e:
            _logger.critical(e)
            exit(0)
