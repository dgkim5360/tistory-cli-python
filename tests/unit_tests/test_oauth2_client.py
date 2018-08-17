from unittest.mock import Mock, MagicMock
import urllib.request

from tistory.oauth2 import client, token


def test_get_access_token(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(token, 'get_client_id', Mock(return_value='CLIENT_ID'))
        m.setattr(token,
                  'get_client_secret',
                  Mock(return_value='CLIENT_SECRET'))
        m.setattr(token,
                  'get_redirect_uri',
                  Mock(return_value=('localhost', 8000)))
        m.setattr(token, 'set_access_token', Mock())
        urlopen = MagicMock(spec=urllib.request.urlopen)
        urlopen.return_value.__enter__.return_value.read.return_value = b'a=1'
        m.setattr(urllib.request, 'urlopen', urlopen)

        code = 'CODE'
        client.get_access_token(code)

        token.get_client_id.assert_called_once()
        token.get_client_secret.assert_called_once()
        token.get_redirect_uri.assert_called_once()
        token.set_access_token.assert_called_once_with(b'1')
