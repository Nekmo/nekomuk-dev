#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
try:
    from . import db
except:
    import sys
    import os
    sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))
    import db

import __main__

if 'sql_file' in dir(__main__):
    sql_file = __main__.sql_file
else:
    sql_file = 'db.sqlite3'
sql = db.SQL(sql_file)

class Server(object):
    methods = ['search', 'ping']

    def method_search(self, get, post):
        query = get['query'][0]
        query = '%%%s%%' % query
        sentence = """\
            SELECT file.name, file.icon, file.relative_root, device.name,
                   file.type
            FROM file INNER JOIN device ON device.id = file.device
            WHERE file.name LIKE ? ORDER BY file.name
        """
        resp = sql.c.execute(sentence, (query,))
        return {'files': list(resp)}

    def method_ping(self,get, post):
        return 'PONG'


class IORequest(Server):
    def get(self, request, pypath):
        if not 'method' in request.get:
            return request.send('Please, select a method')
        method = request.get['method'][0]
        if not method in self.methods:
            return request.send('Method not valid')
        body = getattr(self, 'method_' + method)(request.get, request.post)
        if isinstance(body, (list, dict, tuple)):
            body = json.dumps(body)
        request.send(body)

