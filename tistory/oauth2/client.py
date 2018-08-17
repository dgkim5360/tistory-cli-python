import urllib.parse
import urllib.request
import urllib.error

from . import token

URL_TISTORY_TOKEN = 'https://www.tistory.com/oauth/access_token'


def get_access_token(code: str):
    client_id = token.get_client_id()
    client_secret = token.get_client_secret()
    host, port = token.get_redirect_uri()
    redirect_uri = 'http://{}:{}'.format(host, port)

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code,
        'grant_type': 'authorization_code',
    }
    data = urllib.parse.unquote(urllib.parse.urlencode(data))
    data = data.encode('ascii')
    request = urllib.request.Request(URL_TISTORY_TOKEN, data)

    with urllib.request.urlopen(request) as response:
        response_raw = response.read()

    access_token = response_raw.split(b'=')[1]
    token.set_access_token(access_token)
