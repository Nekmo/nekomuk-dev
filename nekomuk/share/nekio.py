#!/usr/bin/env python2
print("Content-Type: application/json")
print('')
import cgi

try:
    from nekomuk import ioserver
except ImportError:
    import sys
    import os
    sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
    # for key, value in os.environ.items(): print '%s => %s' % (key, value)
    sql_file = os.environ.get('NEKOMUK_SQLITE', 'db.sqlite3')
    import ioserver

class Request(object):
    def __init__(self):
        self.post = {}
        self.get = {}
        form = cgi.FieldStorage()
        for key in form:
            self.post[key] = form.getlist(key)
        data = os.environ['REQUEST_URI'].split('?')
        if not len(data) > 1: return
        data = data[1]
        for pair in data.split('&'):
            key, value = pair.split('=')
            if not key in self.get: self.get[key] = []
            self.get[key].append(value)

    def send(self, text):
        print(text)

iorequest = ioserver.IORequest()
iorequest.get(Request(), False)