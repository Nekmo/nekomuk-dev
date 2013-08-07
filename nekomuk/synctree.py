#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
import logging
import mimetypes
import csv
import time
from lxml import etree

from . import filter
from filestree import RenderXML
from render import humanize
from . import db
# from render import render, write_render

# Importar solamente si se va a sincronizar
from filestree import Tree

from infodevice import InfoDevice
infodevice = InfoDevice()

if sys.version_info < (3,0):
    import urllib as parse
else:
    from urllib import parse

class Device(RenderXML):
    _xml_structure = {'name': 'device', 'sub': {
        'plus_quote_name': {'name': 'quote_name', 'sub': {}},
        'code_name': {'name': 'name', 'sub': {}},
    }}
    interfaces = set((
        'type', 'code_name', 'size', 'human_size', 'mean_size',
        'human_mean_size', 'last_update', 'filetype', 'plus_quote_name',
        'icon',
    ))
    icon = 'device.svg'
    filetype = 'device'
    def __init__(self, elem, synctree):
        self.Synctree = synctree
        if elem.attrib.get('label', False):
            self.synctree = synctree
            self.type = 'label'
            self.name = elem.attrib['label']
            device_data = infodevice.get_device_by_label(self.name)
            self.code_name = 'l/%s/%s'
        else:
            self.type = 'uuid'
            self.name = elem.attrib['uuid']
            device_data = infodevice.get_device_by_uuid(self.name)
            self.code_name = 'u/%s/%s'
        self.path = elem.attrib['path']
        self.code_name = self.code_name % (self.name, self.path)
        self.quote_name = parse.quote_plus(self.code_name)
        if not device_data:
            self.available = False
            return
        self.available = True
        self.mount_path = device_data['path']
        self.complete_path = os.path.join(device_data['path'], self.path)
        if self.complete_path.endswith('/'):
            self.complete_path = self.complete_path[:-1]
        if not elem.findall('filesfilter'):
            filesfilter = synctree.filesfilter
        else:
            filesfilter = filter.Filters(
                elem.findall('filesfilter'), synctree=synctree, device=self
            )
        if not elem.findall('dirsfilter'):
            dirsfilter = synctree.dirsfilter
        else:
            dirsfilter = filter.Filters(
                elem.findall('dirsfilter'), synctree=synctree, device=self
            )
        self.tree = Tree(
            self.complete_path, dirsfilter=dirsfilter, filesfilter=filesfilter,
            device=self
        )

    @property
    def last_update(self):
        return time.time()

    @property
    def size(self):
        return self.tree.paths[''].size

    @property
    def human_size(self):
        return humanize(self.size)

    @property
    def mean_size(self):
        return self.tree.paths[''].mean_size

    @property
    def human_mean_size(self):
        return humanize(self.mean_size)

    @property
    def plus_quote_name(self):
        return parse.quote(self.quote_name)

class Home(RenderXML):
    _xml_structure = {'name': 'home', 'sub': {}}
    interfaces = set(('device', 'total'))
    def __init__(self, sql):
        self.sql = sql

    @property
    def device(self):
        devices = []
        for name, id in self.sql.devices.items():
            device_data = {'name': parse.unquote(name), 'id': id}
            device_data['name_quote'] = parse.quote(name)
            if device_data['name'][0] == 'l':
                device_data['method'] = 'label'
            elif device_data['name'][0] == 'u':
                device_data['method'] = 'uuid'
            else:
                device_data['method'] = 'not_implemented'
            device_data['method_value'] = device_data['name'].split('/', 2)[1]
            device_data['path'] = device_data['name'].split('/', 2)[2]
            devices.append(device_data)
            device_data['nfiles'] = list(self.sql.c.execute('''\
                SELECT COUNT(*) FROM file WHERE file.type != 'dir' and
                device == ?;
            ''', (id,)))[0][0]
            device_data['ndirs'] = list(self.sql.c.execute('''\
                SELECT COUNT(*) FROM file WHERE file.type == 'dir' and
                device == ?;
            ''', (id,)))[0][0]
        return devices

    @property
    def total(self):
        data = {}
        data['nfiles'] = list(self.sql.c.execute('''\
            SELECT COUNT(*) FROM file WHERE file.type != 'dir';
        '''))[0][0]
        data['ndirs'] = list(self.sql.c.execute('''\
            SELECT COUNT(*) FROM file WHERE file.type == 'dir';
        '''))[0][0]
        return data

class Devices(Home):
    _xml_structure = {'name': 'dir', 'sub': {'dirs':
        {'name': 'dirs', 'sub': {
            'name': 'dir', 'sub': {},
        }}
    }}
    interfaces = set((
        'name', 'size', 'files', 'dirs', 'root_level', 'quote_name',
        'human_size', 'human_mean_size', 'mean_size', 'icon', 'mtime',
    ))
    _ignore_in_parent = set((
        'files','dirs', 'root_level', 'device_name', 'quote_device',
        'path_dirs'
    ))
    files = []
    icon = 'root.svg'
    root_level = '../'
    name = 'Dispositivos'
    quote_name = 'dispositivos'

    def __init__(self, sql, devices):
        self.sql = sql
        self.devices = devices

    @property
    def dirs(self):
        return self.devices

    @property
    def size(self):
        return 0

    @property
    def human_size(self):
        return humanize(self.size)

    @property
    def mean_size(self):
        if not self.total['nfiles']: return 0
        return self.size / self.total['nfiles']

    @property
    def human_mean_size(self):
        return humanize(self.mean_size)

    @property
    def mtime(self):
        return 0

class SyncTree(object):
    def make_dirs(self):
        dirs = [
            'devices',
            's',
            'stats',
        ]
        for dir in dirs:
            if os.path.exists(dir): continue
            os.makedirs(dir)
        
    def command_sync(self, args):
        mimetypes.init()
        self.filesfilter = filter.Filters(
            self.cfg.findall('globaloptions/filesfilter/*'),
            synctree=self
        )
        self.dirsfilter = filter.Filters(
            self.cfg.findall('globaloptions/dirsfilter/*'),
            synctree=self
        )
        for mimetype in self.cfg.findall('globaloptions/mimetypes/mimetype'):
            mimetypes.add_type(mimetype.attrib['type'], mimetype.attrib['ext'])
        self.make_dirs()
        devices = []
        sql = db.SQL()
        for device in self.cfg.findall('devices/device'):
            devices.append(Device(device, self))
        for device in devices:
            if not device.available:
                logging.info(
                    'El dispositivo %s no se encuentra disponible.' % device.name
                )
                continue
            if not device.tree.paths:
                continue
            html_device_path = os.path.join('devices', device.quote_name)
            if not os.path.exists(html_device_path):
                os.makedirs(html_device_path)
            # Se crea la BD CSV
            csv_file = open(os.path.join(html_device_path, 'data.csv'), 'wb')
            csv_file = csv.writer(csv_file)
            # Se purga la BD SQL para evitar entradas repetidas
            sql.purge_device(device.quote_name)
            for dir in reversed(sorted(device.tree.paths.values())):
                project_dir = os.path.join(html_device_path, dir.relative_root)
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir)
                render_path = os.path.join(project_dir, 'index.xml')
                if os.path.exists(render_path):
                    dir.last_render = etree.parse(open(render_path)).getroot()
                if not dir.update_required:
                    dir.render(project_dir)
                csv_file.writerow([dir.name, 'dir', dir.relative_root])
                sql.add_file(dir)
                sql.add_file(dir.files)
                for file in dir.files:
                    csv_file.writerow([file.name, file.icon, dir.relative_root])
                # write_render(
                #     os.path.join(project_dir, 'index.html'), 
                #     'dir_device.html',
                #     {
                #         'dir': dir,
                #         'device': device,
                #         'root_level': '../../' + dir.relative_level * '../',
                #     },
                # )
            sql.commit()
        home = Home(sql)
        home.render('', 'home.xsl')
        Devices(sql, devices).render('devices', 'dir.xsl')
        sql.close()
        # write_render('index.html')