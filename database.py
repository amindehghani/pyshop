import config
import mysql.connector
import logging
import coloredlogs

_logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=_logger, fmt="%(levelname)s -> %(message)s")


class Database:
    db_auth = False
    TABLES = {
        "Product": {
            "id": "INT(10) PRIMARY KEY",
            "name": "VARCHAR(120)",
            "price": "DOUBLE",
            "description": "LONGTEXT"
        },
        "User": {
            "id": "INT(10) PRIMARY KEY",
            "email": "VARCHAR(120)",
            "password": "VARCHAR(255)"
        }
    }

    def _create_or_select_tables(self):
        db = mysql.connector.connect(
            host=self.db_auth['db_host'],
            user=self.db_auth['db_user'],
            password=self.db_auth['db_password'],
            database=self.db_auth['db_name']
        )
        cursor = db.cursor()
        for table in self.TABLES.keys():
            query = ''
            for row, value in self.TABLES[table].items():
                query += '%s %s,' % (row, value)
            query = query.rstrip(',')
            cursor.execute("CREATE TABLE IF NOT EXISTS %s (%s);" % (table, query))
        db.close()

    def _create_or_select_db(self):
        db = mysql.connector.connect(
            host=self.db_auth['db_host'],
            user=self.db_auth['db_user'],
            password=self.db_auth['db_password'],
        )
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % self.db_auth['db_name'])
        db.close()

    def connect_db(self):
        self.db_auth = config.ConfigParser.get_config('DATABASE', ['db_host', 'db_name', 'db_user', 'db_password'])
        _logger.info("Checking / Creating Database : %s" % self.db_auth['db_name'])
        self._create_or_select_db()
        _logger.info("Checking / Creating Tables for Database : %s" % self.db_auth['db_name'])
        self._create_or_select_tables()
        _logger.info("Connected to database %s successfully." % self.db_auth['db_name'])
        db = mysql.connector.connect(
            host=self.db_auth['db_host'],
            user=self.db_auth['db_user'],
            password=self.db_auth['db_password'],
        )
        cursor = db.cursor()
        return db, cursor
