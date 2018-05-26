class User:
    def __init__(self, username=None, name=None):
        self.username = username
        self.name = name
        self.location = None
        self.status = None

    @staticmethod
    def create_user_list(users_from_api):
        """Create a list of users from an API call. This list will only have their username and name set."""
        users = list()

        for json_user in users_from_api:
            username = json_user['user']['username']
            name = json_user['user']['name']
            user = User(username, name)
            users.append(user)

        return users

    def set_user_info(self, user_info):
        """Set the user info from an API call"""
        user = user_info['user']
        self.username = user['username']
        self.name = user['name']
        self.location = user.get('location', None)

        self.status = 'unknown'
