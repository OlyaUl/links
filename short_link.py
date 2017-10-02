#! env bin/python
# codding = utf-8
from wsgiref.simple_server import make_server
import hashlib
import psycopg2


def new_link(long_link):
    link_encode = str(long_link).encode('UTF-8')
    link_bytes = bytes(link_encode)
    link_hash = hashlib.md5(link_bytes)
    md5_link = link_hash.hexdigest()
    return md5_link


def save_links(short_link, long_link):
    connect = psycopg2.connect(database='links', user='postgres', host='127.0.0.1', password='1')
    cursor = connect.cursor()
    cursor.execute(
        'INSERT INTO public.link ( long_link, hash_link) '
        ' VALUES (%s, %s)',
        [short_link, long_link])

    connect.commit()
    cursor.close()
    connect.close()


def get_long_link(short_link):
    connect = psycopg2.connect(database='links', user='postgres', host='127.0.0.1', password='1')
    cursor = connect.cursor()
    cursor.execute("SELECT long_link FROM link WHERE hash_link=%s", [short_link])
    link = cursor.fetchall()
    cursor.close()
    connect.close()
    return link


link = 'http://hlabs.org/development/python/wsgi123.html'
a = new_link(link)
print(a)
save_links(link, a)
b = get_long_link(a)
print(b)


def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    index = """<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Links</title>
            </head>
            <body>
            <form >

              <input type="text" name="link">Link</p>
              <p><input type="submit"></p>
             </form>
            </body>
            </html>"""

    return [index.encode()]


httpserv = make_server('localhost', 8080, app)
httpserv.serve_forever()
