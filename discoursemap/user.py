import logging
from urllib.parse import urljoin

from discoursemap.config import Config

logger = logging.getLogger(__name__)


class User:
    def __init__(self, id, username=None, name=None):
        self.id = id
        self.username = username
        self.name = name
        self.avatar = None
        self.location = None
        self.active = None

    @staticmethod
    def create_user_list(users_from_api):
        """Create a list of users from an API call. This list will only have their username and name set."""
        users = dict()

        for json_user in users_from_api:
            id = json_user['id']

            # Add user if it doesn't already exist
            if not users.get(id):
                username = json_user['user']['username']
                name = json_user['user']['name']
                user = User(id, username, name)
                users.setdefault(id, user)

        return users

    def set_user_info(self, user_info):
        """Set the user info from an API call"""
        user = user_info['user']
        self.username = user['username']
        self.name = user['name']
        self.location = user.get('location', None)
        if user.get('suspend_reason', None):
            self.active = False
        else:
            self.active = True

        avatar = user.get('avatar_template', None)
        # Change '{size}' to 120
        if avatar:
            self.avatar = urljoin(Config.SERVER_URL, avatar.replace('{size}', '120'))