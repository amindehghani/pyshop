import coloredlogs
import database
import logging
import secrets

from web import app

_logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=_logger, fmt="%(levelname)s -> %(message)s")


def main():
    _logger.info("Starting Service...")
    _logger.info("Connecting to Database...")
    db_helper = database.Database()
    db, cursor = db_helper.connect_db()
    app.config['db_cursor'] = cursor
    app.config['db'] = db
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.run()


if __name__ == '__main__':
    main()
