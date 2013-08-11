#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import shutil
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

log = logging.getLogger('nekomuk')

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
        about_xml = os.path.join('devices', self.quote_name, 'about.xml')
        if os.path.exists(about_xml):
            self.about_root = etree.parse(open(about_xml)).getroot()
        else:
            self.about_root = False

    @property
    def last_update(self):
        if self.available: return time.time()
        if not self.about_root: return False
        return self.about_root.find('last_update').text

    @property
    def size(self):
        if self.available: return self.tree.paths[''].size
        if not self.about_root: return False
        return self.about_root.find('size').text

    @property
    def human_size(self):
        if self.available: return humanize(self.size)
        if not self.about_root: return False
        return self.about_root.find('human_size').text

    @property
    def mean_size(self):
        if self.available: return self.tree.paths[''].mean_size
        if not self.about_root: return False
        return self.about_root.find('mean_size').text

    @property
    def human_mean_size(self):
        if self.available: return humanize(self.mean_size)
        if not self.about_root: return False
        return self.about_root.find('human_mean_size').text

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
        # for 
        pass

class SyncTree(object):
    def make_dirs(self):
        dirs = [
            'devices',
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
        devices_quote_names = []
        sql = db.SQL()
        for device in self.cfg.findall('devices/device'):
            device_inst = Device(device, self)
            devices.append(device_inst)
            devices_quote_names.append(device_inst.quote_name)
        # Limpiar la BD de devices que ya no se encuentren en la configuración
        for sql_device in sql.devices.keys():
            if sql_device in devices_quote_names: continue
            sql.delete_device(sql_device)
        # Borrar los directorios 
        for dir_device in os.listdir('devices'):
            if dir_device in devices_quote_names: continue
            if not os.path.isdir(dir_device): continue
            shutil.rmtree(os.path.join('devices', dir_device))
        for device in devices:
            if not device.available:
                log.info(
                    'El dispositivo %s no se encuentra disponible.' % device.code_name
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
            sql.commit()
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
            sql.commit()
            device.render(os.path.join('devices', device.quote_name), False, 'about')
            log.info('Se ha terminado de analizar %s' % device.code_name)
        home = Home(sql)
        home.render('', 'home.xsl')
        Devices(sql, devices).render('devices', 'dir.xsl')
        sql.close()
