#!/usr/bin/env python3 

import argparse
import bookmarks_parser
import getpass
import sys
import urllib.parse
import urllib.request

def create_auth_opener(username, password, url):
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, username, password)
    auth_handler = urllib.request.HTTPDigestAuthHandler(p)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)

def process_bookmark(bookmark_url, yacy_url):
    values = {
        'crawlingDepth': '0',
        'crawlingMode': 'url',
        'crawlingURL': bookmark_url,
        'crawlingstart': '',
        'deleteold': 'off',
        'indexMedia': 'on',
        'indexText': 'on',
        'recrawl': 'reload',
        'reloadIfOlderNumber': '7',
        'reloadIfOlderUnit': 'day'
    }

    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(yacy_url, data)

    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(f'HTTPError: {e.code} - {e.reason}')
        if e.code == 401:
            print('Login required. Stopping.')
            sys.exit(1)
    except urllib.error.URLError as e:
        print(f'URLError: {e.reason}')
    except Exception as e:
        print(f'Error: {str(e)}')

def get_bookmark_urls(dirs):
    urls = []
    for level in dirs:
        urls.extend(
            bookmark['url'] for bookmark in level.get('children', []) if 'url' in bookmark
        )
    return urls

def process_bookmarks(dirs, host, username, password):
    yacy_url = f'{host}/Crawler_p.html'
    print(f'Processing bookmarks for host: {host}')
    if username and password:
        create_auth_opener(username, password, yacy_url)

    bookmark_urls = get_bookmark_urls(dirs)
    for bookmark_url in bookmark_urls:
        print(f'Processing bookmark: {bookmark_url}')
        process_bookmark(bookmark_url, yacy_url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='YaCy instance URL', default='http://localhost:8090')
    parser.add_argument('--file', help='The bookmarks file', required=True)
    parser.add_argument('--username', help='Username for authentication')
    args = parser.parse_args()

    username = args.username
    password = getpass.getpass(prompt='Password: ') if username else None

    dirs = bookmarks_parser.parse(args.file)
    process_bookmarks(dirs, args.host, username, password)

if __name__ == '__main__':
    sys.exit(main())
