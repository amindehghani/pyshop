import coloredlogs
import database
import logging

_logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=_logger, fmt="%(levelname)s -> %(message)s")


def main():
    _logger.info("Starting Service...")
    _logger.info("Connecting to Database...")
    db_helper = database.Database()
    db_helper.connect_db()

if __name__ == '__main__':
    main()
