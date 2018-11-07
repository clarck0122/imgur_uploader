from imgurpython import ImgurClient
from helpers import get_input, get_config
import os


class auth():
    def __init__(self):
        # Get client ID and secret from auth.ini
        # config = get_config()
        # config.read('auth.ini')
        self.client_id = os.environ.get('Client_ID')
        self.client_secret = os.environ.get('Client_Secret')
        self.client = ImgurClient(self.client_id, self.client_secret)

        # Authorization flow, pin example (see docs for other auth types)
        self.authorization_url = self.client.get_auth_url('pin')

        print("Go to the following URL: {0}".format(self.authorization_url))

        # Read in the pin, handle Python 2 or 3 here.
        pin = get_input("Enter pin code: ")

        # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
        credentials = self.client.authorize(pin, 'pin')
        self.client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

        print("Authentication successful! Here are the details:")
        print("   Access token:  {0}".format(credentials['access_token']))
        print("   Refresh token: {0}".format(credentials['refresh_token']))


# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
    auth = auth()