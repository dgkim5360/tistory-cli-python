import json
import sys
import urllib.parse
import urllib.request

from .oauth2 import token


def category():
    if len(sys.argv) < 3:
        print('Usage: tistory category <blog_name>',
              file=sys.stderr)
        return
    blog_name = sys.argv[2]

    access_token = token.get_access_token()
    if access_token is None:
        print('The access token does not exist.\n'
              'Please login first.',
              file=sys.stderr)
        return
    base_url = 'https://www.tistory.com/apis/category/list'
    data = {
        'access_token': access_token,
        'blogName': blog_name,
        'output': 'json',
    }
    data = urllib.parse.urlencode(data)
    full_url = '?'.join([base_url, data])
    request = urllib.request.Request(full_url)

    with urllib.request.urlopen(request) as response:
        response_raw = response.read()
    response_json = json.loads(response_raw.decode())
    categories = response_json['tistory']['item']['categories']

    print('ID\tName')
    print('--\t----')
    for item in categories:
        print('{}\t{}'.format(item['id'], item['name']))
