import config
import mysql.connector


class Database:
    db_auth = False
    TABLES = {
        "Product": {
            "id": "INT(10)",
            "name": "VARCHAR(120)",
            "price": "DOUBLE",
            "description": "LONGTEXT",
            "PRIMARY KEY": "(id)"
        },
        "User": {
            "id": "INT(10)",
            "email": "VARCHAR(120)",
            "password": "VARCHAR",
            "PRIMARY KEY": "(id)"
        }
    }

    def _check_db_exists(self):
        db = mysql.connector.connect(
            host=self.db_auth['db_host'],
            user=self.db_auth['db_user'],
            password=self.db_auth['db_password'],
        )
        cursor = db.cursor()
        cursor.execute("SHOW DATABASES")

        for database in cursor:
            if database == self.db_auth['db_name']:
                db.close()
                return True
        db.close()
        return False

    def _check_tables_exist(self):
        pass

    def _create_db(self):
        db = mysql.connector.connect(
            host=self.db_auth['db_host'],
            user=self.db_auth['db_user'],
            password=self.db_auth['db_password'],
        )
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE %s" % self.db_auth['db_name'])
        db.close()

    def connect_db(self):
        self.db_auth = config.ConfigParser.get_config('DATABASE', ['db_host', 'db_name', 'db_user', 'db_password'])
        db_exists = self._check_db_exists()
        if not db_exists:
            self._create_db()
        tables_exist = self._check_tables_exist()
