import logging

from .config import Config
from .api import Api

logger = logging.getLogger(__name__)


def main():
    api = Api(Config.SERVER_URL, Config.API_USERNAME, Config.API_KEY)
    users = api.get_user('Matteus')


main()