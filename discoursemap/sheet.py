from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import logging
import os

from discoursemap.config import Config

logger = logging.getLogger(__name__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Sheet:
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        CLIENT_SECRETS_FILE = os.path.join(__location__, 'client_secret.json')
        CREDENTIALS_FILE = os.path.join(__location__, 'credentials.json')
        store = file.Storage(CREDENTIALS_FILE)
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

    def update_users(self, sheet_name, users):
        """Update all the users for the specified sheet"""

        # Create user value body
        values = list()
        for user in users.values():
            if user.location:
                column = [user.name, user.location]
                if user.avatar:
                    column.append(user.avatar)
                else:
                    column.append('')
                values.append(column)

        # Add empty rows at the bottom (if users are suspended we want to remove any extras)
        for i in range(20):
            values.append(['','',''])

        value_count = str(len(values)+1)
        sheet_range = sheet_name+'!A2:C'+value_count
        body = {
            'values': values
        }
        logger.debug("body: " + str(body))

        request = self.service.spreadsheets().values().update(
            spreadsheetId=Config.SHEET_ID,
            range=sheet_range,
            valueInputOption='RAW',
            body=body,
        )
        response = request.execute()
