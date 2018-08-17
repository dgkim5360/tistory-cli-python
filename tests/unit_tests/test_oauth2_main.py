import getpass
from unittest.mock import Mock

from tistory.oauth2 import main, server, token


def test_login_for_the_first_time(monkeypatch):
    with monkeypatch.context() as m:
        credential = 'CREDENTIAL'
        credential_bytes = credential.encode()
        m.setattr(getpass, 'getpass', Mock(return_value=credential))
        m.setattr(token,
                  'get_redirect_uri',
                  Mock(return_value=('localhost', 8888)))
        m.setattr(token, 'get_client_id', Mock(return_value=None))
        m.setattr(token, 'set_client_id', Mock())
        m.setattr(token, 'get_client_secret', Mock(return_value=None))
        m.setattr(token, 'set_client_secret', Mock())
        m.setattr(token, 'get_access_token', Mock(return_value=None))
        m.setattr(server, 'run', Mock())

        main.login()

        token.get_redirect_uri.assert_called_once()
        token.get_client_id.assert_called_once()
        token.set_client_id.assert_called_once_with(credential_bytes)
        token.get_client_secret.assert_called_once()
        token.set_client_secret.assert_called_once_with(credential_bytes)
        token.get_access_token.assert_called_once()
        server.run.assert_called_once()


def test_login_after_logout(monkeypatch):
    with monkeypatch.context() as m:
        credential = 'CREDENTIAL'
        m.setattr(getpass, 'getpass', Mock(return_value=credential))
        m.setattr(token,
                  'get_redirect_uri',
                  Mock(return_value=('localhost', 8888)))
        m.setattr(token, 'get_client_id', Mock(return_value=credential))
        m.setattr(token, 'set_client_id', Mock())
        m.setattr(token, 'get_client_secret', Mock(return_value=credential))
        m.setattr(token, 'set_client_secret', Mock())
        m.setattr(token, 'get_access_token', Mock(return_value=None))
        m.setattr(server, 'run', Mock())

        main.login()

        token.get_redirect_uri.assert_called_once()
        token.get_client_id.assert_called_once()
        token.set_client_id.assert_not_called()
        token.get_client_secret.assert_called_once()
        token.set_client_secret.assert_not_called()
        token.get_access_token.assert_called_once()
        server.run.assert_called_once()


def test_login_after_login(monkeypatch):
    with monkeypatch.context() as m:
        credential = 'CREDENTIAL'
        m.setattr(getpass, 'getpass', Mock(return_value=credential))
        m.setattr(token,
                  'get_redirect_uri',
                  Mock(return_value=('localhost', 8888)))
        m.setattr(token, 'get_client_id', Mock(return_value=credential))
        m.setattr(token, 'set_client_id', Mock())
        m.setattr(token, 'get_client_secret', Mock(return_value=credential))
        m.setattr(token, 'set_client_secret', Mock())
        m.setattr(token, 'get_access_token', Mock(return_value=credential))
        m.setattr(server, 'run', Mock())

        main.login()

        token.get_redirect_uri.assert_called_once()
        token.get_client_id.assert_called_once()
        token.set_client_id.assert_not_called()
        token.get_client_secret.assert_called_once()
        token.set_client_secret.assert_not_called()
        token.get_access_token.assert_called_once()
        server.run.assert_not_called()


def test_logout(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(token, 'delete_access_token', Mock())

        main.logout()

        token.delete_access_token.assert_called_once()


def test_purge(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(token, 'delete_client_id', Mock())
        m.setattr(token, 'delete_client_secret', Mock())
        m.setattr(token, 'delete_access_token', Mock())

        main.logout()

        token.delete_access_token.assert_called_once()
        token.delete_access_token.assert_called_once()
        token.delete_access_token.assert_called_once()
