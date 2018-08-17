from unittest.mock import Mock
import http.server

from tistory.oauth2 import server


def test_run(monkeypatch):
    with monkeypatch.context() as m:
        httpserver = Mock()
        m.setattr(http.server, 'HTTPServer', Mock(return_value=httpserver))

        host, port = 'localhost', 8000
        server.run(host, port)

        http.server.HTTPServer.assert_called_with((host, port),
                                                  server.OauthRedirectHandler)
        httpserver.serve_forever.assert_called_once()
