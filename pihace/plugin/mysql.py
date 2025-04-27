import mysql.connector
from mysql.connector import Error

class MySQL:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def __call__(self):
        try:
            # Parse the DSN to get host, user, password, and database
            user, pwd, host, port, db = self._parse_dsn(self.dsn)
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=pwd,
                database=db,
                port=port,
                auth_plugin='mysql_native_password'
            )

            if connection.is_connected():
                return True
            else:
                return (False, "Unable to connect to MySQL.")
        except Error as e:
            return (False, str(e))

    def _parse_dsn(self, dsn):
        # Assumes dsn format is mysql://user:password@host:port/database
        parts = dsn.split('@')
        user_pwd = parts[0][8:].split(':')
        user = user_pwd[0]
        pwd = user_pwd[1]
        host_port_db = parts[1].split(':')
        host = host_port_db[0]
        port_db = host_port_db[1].split('/')
        port = int(port_db[0])
        db = port_db[1]

        return user, pwd, host, port, db
