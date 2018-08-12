import json
import os
import sys
import urllib.parse
import urllib.request

import mistune

from .oauth2 import token


def post():
    if len(sys.argv) != 5:
        print('Usage: tistory post <blog_name> <category_id> <file_path>',
              file=sys.stderr)
        return
    blog_name, category_id, file_path = sys.argv[2:]

    access_token = token.get_access_token()
    if access_token is None:
        print('The access token does not exist.\n'
              'Please login first.',
              file=sys.stderr)
        return

    if not os.path.isfile(file_path):
        print('The file {} not found.'.format(file_path),
              file=sys.stderr)
        return
    dir_name, file_name = os.path.split(file_path)
    slogan, file_ext = os.path.splitext(file_name)

    with open(file_path) as fp:
        title = fp.readline()
        fp.readline()
        content_md = fp.read()
    content_html = mistune.markdown(content_md)

    base_url = 'https://www.tistory.com/apis/post/write'
    data = {
        'access_token': access_token,
        'blogName': blog_name,
        'title': title,
        'category': category_id,
        'content': content_html,
        'slogan': slogan,
        'output': 'json',
    }
    data = urllib.parse.urlencode(data).encode('ascii')
    request = urllib.request.Request(base_url, data)

    with urllib.request.urlopen(request) as response:
        response_raw = response.read()
    response_json = json.loads(response_raw.decode())

    status_code = response_json['tistory']['status']
    if status_code != '200':
        print('Got HTTP error {}.'.format(status_code))
        return
    print('Successfully uploaded.')

    post_id = response_json['tistory']['postId']
    file_path_renamed = os.path.join(dir_name,
                                     '{}_{}'.format(post_id, file_name))
    os.rename(file_path, file_path_renamed)
    print('{} is renamed with post_id\nas {}.'.format(file_path,
                                                      file_path_renamed))
