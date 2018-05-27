import logging

from .config import Config
from .api import Api
from .user import User
from .sheet import Sheet

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def get_all_users():
    api = Api(Config.SERVER_URL, Config.API_USERNAME, Config.API_KEY)
    users_api_list = api.get_users()
    users = User.create_user_list(users_api_list)

    for user in users.values():
        user_info = api.get_user_info(user.username)
        user.set_user_info(user_info)

    return users


def update_sheet(users):
    # Remove suspended users
    if not Config.SHOW_SUSPENDED:
        users_old = users
        users = dict()
        for user in users_old.values():
            if user.active:
                users.setdefault(user.id, user)

    sheet = Sheet()
    sheet.update_users(Config.SHEET_NAME, users)


def main():
    users = get_all_users()
    update_sheet(users)

main()