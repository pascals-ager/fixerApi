from configuration import ApiConfiguration
import requests


class ApiClient(object):

    def __init__(self, host):
        self.config = ApiConfiguration()
        self.host = host
        self.api_key = self.config.api_key
        self.rest_client = requests

    def request(self, method, url, query_params=None):
        if method == "GET":
            return self.rest_client.get(url, query_params)
        else:
            raise ValueError("http method not implemented")

    def call_api(self, resource_path, method, query_params=None):
        url = self.host + '/' + resource_path
        query_params = (('access_key', self.api_key), ) + query_params

        response_data = self.request(method, url, query_params)
        return response_data
