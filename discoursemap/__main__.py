import logging

from .config import Config
from .api import Api
from .user import User

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def main():
    api = Api(Config.SERVER_URL, Config.API_USERNAME, Config.API_KEY)
    users_api_list = api.get_users()
    users = User.create_user_list(users_api_list)

    for user in users:
        user_info = api.get_user_info(user.username)
        user.set_user_info(user_info)

    logger.debug('All Users:\n' + str(users))

    # TODO Add users with a location to

main()