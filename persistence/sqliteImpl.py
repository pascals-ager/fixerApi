from configuration import DbConfiguration
from datetime import datetime as dt
import logging
import sqlite3
logging.basicConfig(level=logging.INFO, filename="resources/fixerApi.log")


class SqliteImpl:

    def __init__(self, db_name):
        self.logger = logging.getLogger()
        self.config = DbConfiguration()
        self.db_name = db_name
        self.database_uri = "{}/{}".format(self.config.path, db_name)

    def put_ddl(self, statement):
        conn = None
        try:
            logging.info("Connecting to {}".format(self.database_uri))
            conn = sqlite3.connect(self.database_uri)
            conn.execute(statement)
        except sqlite3.Error as e:
            self.logger.error("Database error: {}".format(e))
            raise e
        except Exception as e:
            self.logger.error("Exception in query: {}".format(e))
            raise e
        finally:
            if conn:
                conn.close()

    def persist(self, response, statement):
        conn = None
        try:
            logging.info("Connecting to {}".format(self.database_uri))
            base_currency = response['base']
            conn = sqlite3.connect(self.database_uri)
            cur = conn.cursor()
            for date in response['rates']:
                for code in (response['rates'][date]).keys():
                    cur.execute(statement,
                            (base_currency, dt.strptime(date, "%Y-%m-%d").date(), response['rates'][date][code], code))
                cur.execute('COMMIT')
        except sqlite3.Error as e:
            self.logger.error("Database error: {}".format(e))
            raise e
        except Exception as e:
            self.logger.error("Exception in query: {}".format(e))
            raise e
        finally:
            if conn:
                conn.close()

    def project(self, statement, params=None):
        conn = None
        results = None
        try:
            logging.info("Connecting to {}".format(self.database_uri))
            conn = sqlite3.connect(self.database_uri)
            results = conn.execute(statement, params).fetchall()
        except sqlite3.Error as e:
            self.logger.error("Database error: {}".format(e))
            raise e
        except Exception as e:
            self.logger.error("Exception in query: {}".format(e))
            raise e
        finally:
            if conn:
                conn.close()
            return results


