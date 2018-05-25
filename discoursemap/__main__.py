import logging
from configparser import ConfigParser

from .api import Api

logger = logging.getLogger(__name__)


def main():
    config = ConfigParser()
    config.read('discoursemap/config.ini')

    authentication = config['authentication']
    url = authentication['url']
    username = authentication['username']
    api_key = authentication['api_key']

    logger.debug('Url: ' + url + ', Username: ' + username + ', Key: ' + api_key)

    api = Api(url, username, api_key)
    users = api.get_user('Matteus')


main()