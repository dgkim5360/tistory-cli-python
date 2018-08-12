import os

import secretstorage


FILE_REDIRECT_URI = './.redirect-uri'
SS_CLIENT_ID_LABEL = 'Client ID for Tistory API'
SS_CLIENT_ID_ATTRIBUTE = {
    'application': 'tistory-cli',
    'secret-type': 'client-id',
}
SS_CLIENT_SECRET_LABEL = 'Client Secret for Tistory API'
SS_CLIENT_SECRET_ATTRIBUTE = {
    'application': 'tistory-cli',
    'secret-type': 'client-secret',
}
SS_TOKEN_LABEL = 'Access Token for Tistory API'
SS_TOKEN_ATTRIBUTE = {
    'application': 'tistory-cli',
    'secret-type': 'access-token',
}


def get_redirect_uri():
    if os.path.isfile(FILE_REDIRECT_URI):
        with open(FILE_REDIRECT_URI) as f:
            server_address = f.readline()

        try:
            host, port = server_address.split(':')
            port = int(port)
        except ValueError:
            return ('localhost', 8888)
        return (host, port)

    return ('localhost', 8888)


def get_client_id():
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    searched = coll.search_items(SS_CLIENT_ID_ATTRIBUTE)

    try:
        item = next(searched)
    except StopIteration:
        return None
    else:
        if item.is_locked():
            item.unlock()
        return item.get_secret()


def set_client_id(token: bytes):
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    if coll.is_locked():
        coll.unlock()
    coll.create_item(SS_CLIENT_ID_LABEL,
                     SS_CLIENT_ID_ATTRIBUTE,
                     token,
                     replace=True)


def delete_client_id():
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    searched = coll.search_items(SS_CLIENT_ID_ATTRIBUTE)

    try:
        item = next(searched)
    except StopIteration:
        return None
    else:
        item.delete()
        return True


def get_client_secret():
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    searched = coll.search_items(SS_CLIENT_SECRET_ATTRIBUTE)

    try:
        item = next(searched)
    except StopIteration:
        return None
    else:
        if item.is_locked():
            item.unlock()
        return item.get_secret()


def set_client_secret(token: bytes):
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    if coll.is_locked():
        coll.unlock()
    coll.create_item(SS_CLIENT_SECRET_LABEL,
                     SS_CLIENT_SECRET_ATTRIBUTE,
                     token,
                     replace=True)


def delete_client_secret():
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    searched = coll.search_items(SS_CLIENT_SECRET_ATTRIBUTE)

    try:
        item = next(searched)
    except StopIteration:
        return None
    else:
        item.delete()
        return True


def get_access_token():
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    searched = coll.search_items(SS_TOKEN_ATTRIBUTE)

    try:
        item = next(searched)
    except StopIteration:
        return None
    else:
        if item.is_locked():
            item.unlock()
        return item.get_secret()


def set_access_token(token: bytes):
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    if coll.is_locked():
        coll.unlock()
    coll.create_item(SS_TOKEN_LABEL,
                     SS_TOKEN_ATTRIBUTE,
                     token,
                     replace=True)


def delete_access_token():
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)

    searched = coll.search_items(SS_TOKEN_ATTRIBUTE)

    try:
        item = next(searched)
    except StopIteration:
        return None
    else:
        item.delete()
        return True
