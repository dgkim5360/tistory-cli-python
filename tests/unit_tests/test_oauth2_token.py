from unittest.mock import Mock
import secretstorage

from tistory.oauth2 import token


def item_generator(item):
    yield item


class DummyCollection:
    def __init__(self, item):
        self.is_locked = Mock(return_value=False)
        self.create_item = Mock(return_value=None)
        self.search_items = Mock(return_value=item_generator(item))


class DummyItem:
    def __init__(self):
        self.is_locked = Mock(return_value=False)
        self.get_secret = Mock(return_value='SECRET')
        self.delete = Mock()


def test_get_redirect_uri_default():
    host, port = token.get_redirect_uri()

    assert host == 'localhost'
    assert port == 8888


def test_get_redirect_uri_customized():
    FILE_REDIRECT_URI_ORIGINAL = token.FILE_REDIRECT_URI
    token.FILE_REDIRECT_URI = './tests/.redirect_uri'
    host, port = token.get_redirect_uri()

    assert host == 'localhost'
    assert port == 8000

    token.FILE_REDIRECT_URI = FILE_REDIRECT_URI_ORIGINAL


def test_get_client_id(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        client_id = token.get_client_id()
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.search_items.assert_called_with(token.SS_CLIENT_ID_ATTRIBUTE)
        item.is_locked.assert_called_once()
        item.get_secret.assert_called_once()
        assert client_id == 'SECRET'


def test_set_client_id(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        token.set_client_id('ANOTHER_SECRET')
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.is_locked.assert_called_once()
        coll.create_item.assert_called_with(
            token.SS_CLIENT_ID_LABEL,
            token.SS_CLIENT_ID_ATTRIBUTE,
            'ANOTHER_SECRET',
            replace=True,
        )


def test_delete_client_id(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        result = token.delete_client_id()
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.search_items.assert_called_with(token.SS_CLIENT_ID_ATTRIBUTE)
        item.delete.assert_called_once()
        assert result is True


def test_get_client_secret(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        client_secret = token.get_client_secret()
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.search_items.assert_called_with(token.SS_CLIENT_SECRET_ATTRIBUTE)
        item.is_locked.assert_called_once()
        item.get_secret.assert_called_once()
        assert client_secret == 'SECRET'


def test_set_client_secret(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        token.set_client_secret('ANOTHER_SECRET')
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.is_locked.assert_called_once()
        coll.create_item.assert_called_with(
            token.SS_CLIENT_SECRET_LABEL,
            token.SS_CLIENT_SECRET_ATTRIBUTE,
            'ANOTHER_SECRET',
            replace=True,
        )


def test_delete_client_secret(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        result = token.delete_client_secret()
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.search_items.assert_called_with(token.SS_CLIENT_SECRET_ATTRIBUTE)
        item.delete.assert_called_once()
        assert result is True


def test_get_access_token(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        access_token = token.get_access_token()
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.search_items.assert_called_with(token.SS_TOKEN_ATTRIBUTE)
        item.is_locked.assert_called_once()
        item.get_secret.assert_called_once()
        assert access_token == 'SECRET'


def test_set_access_token(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        token.set_access_token('ANOTHER_SECRET')
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.is_locked.assert_called_once()
        coll.create_item.assert_called_with(
            token.SS_TOKEN_LABEL,
            token.SS_TOKEN_ATTRIBUTE,
            'ANOTHER_SECRET',
            replace=True,
        )


def test_delete_access_token(monkeypatch):
    with monkeypatch.context() as m:
        item = DummyItem()
        coll = DummyCollection(item)
        m.setattr(secretstorage,
                  'dbus_init',
                  Mock(spec=secretstorage.dbus_init))
        m.setattr(secretstorage,
                  'get_default_collection',
                  Mock(return_value=coll))

        result = token.delete_access_token()
        secretstorage.dbus_init.assert_called_once()
        secretstorage.get_default_collection.assert_called_once()
        coll.search_items.assert_called_with(token.SS_TOKEN_ATTRIBUTE)
        item.delete.assert_called_once()
        assert result is True
