from configuration import ServiceConfiguration
from api.apiClient import ApiClient
from persistence.sqliteImpl import SqliteImpl
from _datetime import datetime as dt
import json
import logging
logging.basicConfig(level=logging.INFO, filename="resources/fixerApi.log")


class ServiceImpl:

    def __init__(self):
        self.logger = logging.getLogger()
        self.config = ServiceConfiguration()
        self.source = ApiClient(self.config.host)
        self.destination = SqliteImpl(self.config.db_name)
        self.table = self.config.table_name

    def seed_database(self):
        self.logger.info("Dropping Table if it exists {}".format(self.table))
        drop_statement = "DROP TABLE if exists {}".format(self.table)
        self.destination.put_ddl(drop_statement)
        create_statement = "CREATE TABLE {} (base_code TEXT, date DATE, rate REAL, currency_code TEXT)".format(self.table)
        self.logger.info("Creating Table {} with {}".format(self.table, create_statement))
        self.destination.put_ddl(create_statement)

    def get_timeseries_data(self, parameters):
        resource_path = 'timeseries'
        self.logger.info("Making get requests on /{} using {}".format(resource_path, parameters))
        res = self.source.call_api(resource_path=resource_path, method='GET', query_params=parameters)
        self.logger.info("Successfully retrieved the response for {}".format(parameters))
        return res

    def persist_response(self, response):
        self.logger.info("persisting response from {}".format(response.url))
        response_json = json.loads(response.text)
        insert_stmt = "INSERT INTO {}(base_code , date , rate , currency_code) VALUES (:1, :2, :3, :4)".format(
            self.table)
        self.destination.persist(response=response_json, statement=insert_stmt)
        self.logger.info("Successfully persisted the response into {}".format(self.table))

    def get_average_rate(self, base_code, currency_code, start_date, end_date):
        query = """SELECT base_code, currency_code, AVG(rate) FROM {} where base_code = :1
            AND currency_code = :2 AND date > :3 AND date < :4 GROUP BY base_code, currency_code""".format(
            self.table)
        params = (base_code, currency_code, dt.strptime(start_date, "%Y-%m-%d").date(), dt.strptime(end_date, "%Y-%m-%d").date())
        self.logger.info("fetching results for {} with params {}".format(query, params))
        return self.destination.project(statement=query, params=params)
