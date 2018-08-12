import threading
import http.server
import urllib.parse

from . import client


class OauthRedirectHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        dict_query = urllib.parse.parse_qs(url_parsed.query)

        auth_code = dict_query['code'][0]
        client.get_access_token(auth_code)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        response_html = b"""<html>
<head><title>Tistory-cli</title></head>
<body>
<h1>Successfully Got the Access Token</h1>
<p>Just go back to your terminal :)</p>
</body>
</html>"""
        self.wfile.write(response_html)

        killer = threading.Thread(target=self.server.shutdown,
                                  daemon=True)
        killer.start()


def run(host='localhost', port=8888):
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, OauthRedirectHandler)
    httpd.serve_forever()
