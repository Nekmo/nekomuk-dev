#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
import logging
import mimetypes
import csv
from lxml import etree

from . import filter
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

class Device(object):
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
            html_device_path = os.path.join('devices', device.quote_name)
            if not os.path.exists(html_device_path):
                os.makedirs(html_device_path)
            # Se crea la BD CSV
            csv_file = open(os.path.join(html_device_path, 'data.csv'), 'wb')
            csv_file = csv.writer(csv_file)
            # Se purga la BD SQL para evitar entradas repetidas
            sql.purge_device(device.quote_name)
            for dir in device.tree.paths.values():
                project_dir = os.path.join(html_device_path, dir.relative_root)
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir)
                render_path = os.path.join(project_dir, 'index.xml')
                if os.path.exists(render_path):
                    dir.last_render = etree.parse(open(render_path)).getroot()
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
            sql.close()
        # write_render('index.html')