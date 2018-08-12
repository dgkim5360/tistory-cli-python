import sys

from .oauth2 import main as auth
from . import get
from . import post

USAGE = """USAGE:
    tistory login
    tistory logout
    tistory purge

    tistory category <blog_name>
    tistory post <blog_name> <category_id> <file_path>"""


def main():
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        return

    command = sys.argv[1]
    if command == 'login':
        auth.login()
    elif command == 'logout':
        auth.logout()
    elif command == 'purge':
        auth.purge()
    elif command == 'category':
        get.category()
    elif command == 'post':
        post.post()
    else:
        print(USAGE, file=sys.stderr)
        return
