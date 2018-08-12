import getpass
import urllib

from . import server
from . import token


URL_TISTORY_AUTH = 'https://www.tistory.com/oauth/authorize'


def login():
    print('Checking the .redirect-uri file ...')
    host, port = token.get_redirect_uri()
    redirect_uri = 'http://{}:{}'.format(host, port)
    print('Confirmed:', redirect_uri)

    print('Checking the client ID ...')
    client_id = token.get_client_id()
    if not client_id:
        print('The client ID does not exist.\n'
              'Please insert it here.')
        client_id = getpass.getpass('Client ID:')
        token.set_client_id(client_id.encode())
    print('Done.')

    print('Checking the client secret ...')
    client_secret = token.get_client_secret()
    if not client_secret:
        print('The client secret does not exist.\n'
              'Please insert it here.')
        client_secret = getpass.getpass('Client Secret:')
        token.set_client_secret(client_secret.encode())
    print('Done.')

    print('Checking the access token ...')
    access_token = token.get_access_token()
    if not access_token:
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
        }
        url_values = urllib.parse.urlencode(params)
        print('The access token does not exist.\n'
              'Please visit this login URL.')
        print(URL_TISTORY_AUTH + '?' + urllib.parse.unquote(url_values))
        server.run()

        print('Successfully got the access token.')
    print('Done.')
    print('All Ready.')


def logout():
    print('Removing the access token ...')
    result = token.delete_access_token()
    if result is None:
        print('Not found. Done.')
    elif result is True:
        print('Successfully removed. Done.')


def purge():
    logout()

    print('Removing the client secret ...')
    result = token.delete_client_secret()
    if result is None:
        print('Not found. Done.')
    elif result is True:
        print('Successfully removed. Done.')

    print('Removing the client ID ...')
    result = token.delete_client_id()
    if result is None:
        print('Not found. Done.')
    elif result is True:
        print('Successfully removed. Done.')
    print('Everything is removed.')
