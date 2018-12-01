""" Common database functionality. """

from logging import getLogger

from mysql import connector


class Database():

    def __init__(self, wp_config):
        """
        Database.

        Args:
            wp_config (wpconfigr.WpConfigFile): WordPress configuration.
        """

        self._wp_config = wp_config
        self._log = getLogger(__name__)

    def _connect(self, host_and_port, username, password):
        """
        Gets a connection to the database.

        Args:
            host_and_port (str): Either just a hostname, or a hostname and a
                                 port separated by a colon (":").
            username (str):      Username.
            password (str):      Password.

        Returns:
            MySQLConnection: Database connection.
        """

        host_parts = host_and_port.split(':')
        host = host_parts[0]

        if len(host_parts) == 2:
            port = host_parts[1]
        else:
            port = None

        self._log.info('Attempting to connect to "%s" on port "%s"...',
                       host,
                       port)

        if port:
            return connector.connect(
                engine='InnoDB',
                host=host,
                port=port,
                user=username,
                password=password)

        return connector.connect(
            engine='InnoDB',
            host=host,
            user=username,
            password=password)

    def test_config(self, throw=False):
        """
        Tests the connection details in the WordPress configuration.

        Returns:
            bool: Success.
        """

        try:
            conn = self._connect(host_and_port=self._wp_config.get('DB_HOST'),
                                 username=self._wp_config.get('DB_USER'),
                                 password=self._wp_config.get('DB_PORT'))
            conn.close()
            return True

        except connector.errors.ProgrammingError as error:
            if throw:
                raise error
            return False

    def ensure_database_setup(self, admin_credentials):
        """
        Ensure the database is set up to match the WordPress configuration.

        Args:
            admin_credentials (Credentials): Database admin credentials.
        """

        def sql(statement):
            return statement.format(n=db_name)

        host_and_port = self._wp_config.get('DB_HOST')
        db_name = self._wp_config.get('DB_NAME')
        wp_username = self._wp_config.get('DB_USER')
        wp_password = self._wp_config.get('DB_PASSWORD')

        conn = self._connect(host_and_port=host_and_port,
                             username=admin_credentials.username,
                             password=admin_credentials.password)

        cur = conn.cursor()

        self._log.info('Ensuring database "%s" exists...', db_name)
        # Database names cannot be parameterized, so be careful.
        cur.execute(sql('CREATE DATABASE IF NOT EXISTS {n};'))

        self._log.info('Using database "%s"...', db_name)
        cur.execute(sql('USE {n};'))

        self._log.info('Ensuring user "%s" exists...', wp_username)
        cur.execute(sql('GRANT ALL PRIVILEGES ON {n} TO %s IDENTIFIED BY %s;'),
                    (wp_username, wp_password))

        self._log.info('Flushing privileges...')
        cur.execute('FLUSH PRIVILEGES;')

        self._log.info('Committing transaction...')
        conn.commit()

        self._log.info('Closing cursor...')
        cur.close()

        self._log.info('Closing connection...')
        conn.close()

        self._log.info('Database setup is complete.')
