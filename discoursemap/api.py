import logging
from urllib.parse import urljoin
import urllib3
import certifi

logger = logging.getLogger(__name__)


class Api:
    def __init__(self, url, username, key):
        self.url = url
        self.username = username
        self.key = key
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
        )

    def get_user(self, username):
        return self._get('/users/' + username + '.json')

    def get_active_user_list(self):
        return self._get('/admin/users/list/active.json')

    def get_suspended_user_list(self):
        return self._get('/admin/users/list/suspended.json')

    def get_combined_user_list(self):
        return self.get_active_user_list().extend(self.get_suspended_user_list())

    def _get(self, path):
        return self._api_call('GET', path)

    def _api_call(self, method, path):
        full_url = urljoin(self.url, path)
        logger.debug('Full url: ' + full_url)
        response = self.http.request(
            method,
            full_url,
            fields={
                'api_username': self.username,
                'api_key': self.key,
            },
        )

        logger.debug('Response Status: ' + str(response.status))
        logger.debug('Response Data: ' + str(response.data))