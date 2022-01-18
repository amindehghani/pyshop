import coloredlogs
import database
import logging
import secrets
import pathlib

from web import app

_logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=_logger, fmt="%(levelname)s -> %(message)s")


def main():
    _logger.info("Starting Service...")
    _logger.info("Connecting to Database...")
    db_helper = database.Database()
    db = db_helper.connect_db()
    app.config['db'] = db
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    current_path = pathlib.Path(__file__).parent.resolve()
    app.config['UPLOAD_PATH'] = str(current_path) + '/web/uploads'
    app.run()


if __name__ == '__main__':
    main()
