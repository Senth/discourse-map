from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import logging

from .config import Config

logger = logging.getLogger(__name__)

class Sheet:
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        store = file.Storage('discoursemap/credentials.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('discoursemap/client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

    def update_users(self, sheet_name, users):
        """Update all the users for the specified sheet"""

        # Create user value body
        values = list()
        for user in users.values():
            if user.location:
                values.append([user.name, user.location])

        value_count = str(int(len(values)*1.1))
        range = sheet_name+'!A1:B'+value_count
        body = {
            'values': values
        }
        logger.debug("body: " + str(body))

        request = self.service.spreadsheets().values().update(
            spreadsheetId=Config.SHEET_ID,
            range=range,
            valueInputOption='RAW',
            body=body,
        )
        response = request.execute()

    def get_test(self):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=Config.SHEET_ID,
            range='All!A1:A1'
        ).execute()

        logger.debug("Sheet value: " + str(result.get('values', [])))