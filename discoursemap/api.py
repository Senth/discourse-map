import logging
from urllib.parse import urljoin
import urllib3
import certifi
import json
import queue
import time

from .config import Config

logger = logging.getLogger(__name__)

WAIT_TIME_ON_TOO_MANY_REQUESTS = 10

class Api:
    def __init__(self, url, username, key):
        self.url = url
        self.username = username
        self.key = key
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
        )

    def get_user_info(self, username):
        return self._get('/users/' + username + '.json')

    def get_users(self):
        number_of_users = 10000000
        page = 0
        all_users = list()

        while len(all_users) < number_of_users:
            response_data = self._get_users_page(page)
            number_of_users = response_data['total_rows_directory_items']
            all_users.extend(response_data['directory_items'])
            page += 1

        logger.debug('All users: ' + str(all_users))
        return all_users

    def _get_users_page(self, page):
        parameters = {
            'period': 'daily',
            'order': 'post_count',
            'page': page,
        }
        return self._get('/directory_items.json', parameters)

    def get_active_user_list(self):
        return self._get('/admin/users/list/active.json')

    def get_suspended_user_list(self):
        return self._get('/admin/users/list/suspended.json')

    def get_combined_user_list(self):
        return self.get_active_user_list().extend(self.get_suspended_user_list())

    def _get(self, path, additional_parameters=None):
        return self._api_call('GET', path, additional_parameters)

    def _api_call(self, method, path, additional_parameters):
        full_url = urljoin(self.url, path)

        parameters = {
            'api_username': self.username,
            'api_key': self.key,
        }

        if additional_parameters:
            parameters = {**parameters, **additional_parameters}

        logger.debug('Full url: ' + full_url + ", parameters: " + str(parameters))

        status = 429
        while status == 429:
            response = self.http.request(
                method,
                full_url,
                parameters,
            )
            status = response.status

            logger.debug('Response Status: ' + str(response.status))
            logger.debug('Response Data: ' + str(response.data))

            # Too many requests, wait a few seconds before trying again
            if status == 429:
                time.sleep(WAIT_TIME_ON_TOO_MANY_REQUESTS)
            elif status == 404:
                raise ConnectionError(response.data)

        return json.loads(response.data.decode('utf-8'))