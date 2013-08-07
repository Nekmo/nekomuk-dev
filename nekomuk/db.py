#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sqlite3
import copy

class SQL(object):
    c = None
    conn = None
    devices = {}
    def __init__(self, name='db.sqlite3'):
        self.name = name
        if not os.path.exists(name):
            self.create_tables()
        self._connect()
        self.after_connect()

    def _connect(self):
        self.conn = sqlite3.connect(self.name)
        self.conn.text_factory = str
        self.c = self.conn.cursor()

    def after_connect(self):
        # Construir tabla con los ids de los devices
        self.devices = dict(self.c.execute('SELECT name, id FROM device'))

    def create_tables(self):
        if self.c is None: self._connect()
        tables = [
            '''CREATE TABLE device (id integer primary key autoincrement, name text)''',
            '''CREATE TABLE file
             (name text, icon text, relative_root text, device integer, type text,
             foreign key(device) references device(id) )'''
        ]
        for table in tables:
            self.c.execute(table)

    def add_device(self, device):
        self.c.execute('INSERT INTO device (name) VALUES (?)', (device,))
        id = self.c.execute('SELECT id FROM device WHERE name = ?', (device,))
        id = list(id)[0][0]
        self.devices[device] = id
        self.conn.commit()
        return id

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def purge_device(self, device):
        if not isinstance(device, int):
            device = self.devices.get(device, None)
        if device is None:
            return False
        self.c.execute('DELETE FROM file WHERE device = ?', (device,))

    def add_file(self, registers):
        if not isinstance(registers, (tuple, list)):
            to_execute = [registers]
        else:
            to_execute = copy.copy(registers)
        for i, register in enumerate(to_execute):
            if not register.tree.device.quote_name in self.devices:
                self.add_device(register.tree.device.quote_name)
            device = self.devices[register.tree.device.quote_name]
            if register.parent is None:
                relative_root = ''
            else:
                relative_root = register.parent.relative_root
            to_execute[i] = (
                register.name, register.icon, relative_root, device,
                register.filetype
            )
        self.c.executemany(
            'INSERT INTO file VALUES (?, ?, ?, ?, ?)',
            to_execute
        )
