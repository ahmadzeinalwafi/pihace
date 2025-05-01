# -*- coding: utf-8 -*-
"""pihace.plugins.mysql: MySQL health check plugin using the MySQL Connector."""
import mysql.connector
from mysql.connector import Error

class MySQL:
    """
    A checker class for performing health checks on a MySQL instance.

    Attributes:
        dsn (str): The Data Source Name (DSN) or connection string for MySQL.
    """

    def __init__(self, dsn: str):
        """
        Initialize the MySQL checker with a DSN.

        Args:
            dsn (str): The Data Source Name (DSN) for the MySQL instance.
        """
        self.dsn = dsn

    def __call__(self):
        """
        Perform a health check on the MySQL instance.

        Returns:
            bool: True if the MySQL connection is successful.
            tuple: (False, error message) if the health check fails or an exception occurs.
        """
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
        """
        Parse the DSN string into its components: user, password, host, port, and database.

        Args:
            dsn (str): The Data Source Name (DSN) for MySQL, e.g., 'mysql://user:password@host:port/database'.

        Returns:
            tuple: A tuple containing user, password, host, port, and database.
        """
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
