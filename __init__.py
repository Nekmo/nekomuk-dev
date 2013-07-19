#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
from lxml import etree
import shutil
import logging
from functools import wraps
import nekomuk
from nekomuk import infodevice
from synctree import SyncTree

NEKOMUK_DIR = os.path.dirname(os.path.abspath(nekomuk.__file__))

try:
    # Añadir soporte para autocompletado para input
    # readline no se encuentra disponible en sistemas no-unix.
    import readline
    import glob
    def complete(text, state):
        comp_text = (glob.glob(text+'*')+[None])[state]
        if os.path.exists(comp_text) and os.path.isdir(comp_text):
            comp_text += '/'
        return comp_text
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
except ImportError:
    pass

try:
    # Sintaxis realzada con color
    from termcolor import cprint
except ImportError:
    def cprint(text, color=None, on_color=None, attrs=None, **kwargs):
        print(text)

#class OriginalClass(object):
    #def orin_method(self):
        #return 'ok'
    
    #def run(self):
        #return 'OriginalClass'
    
#class ModifiedClass(object):
    #def run(self):
        #return 'ModifiedClass'
    
#MyNewClass = type('OriginalClass', (ModifiedClass,), dict(OriginalClass.__dict__))

#MyNewClass().run()
#OriginalClass().run()


def required(**req_kwargs):
    def fnct(f):
        @wraps(f)
        def f2(f_, *args, **kwargs):
            for command, value in req_kwargs.items():
                if command == 'min_args':
                    if len(args[0]) >= value: continue
                    f_.log_error(
                        'El mínimo de argumentos con este comando es de'\
                        ' %i argumentos y usted ha proporcionado %i' % \
                        (value, len(args[0]))
                    )
                    return
                elif command == 'max_args':
                    if len(args[0]) <= value: continue
                    f_.log_error(
                        'El máximo de argumentos con este comando es de'\
                        ' %i argumentos y usted ha proporcionado %i' % \
                        (value, len(args[0]))
                    )
                    return
                elif command == 'valid_path':
                    if os.path.exists(args[0][value]): continue
                    f_.log_error('La ruta especificada no existe.')
                    return
                elif command == 'not_valid_path':
                    if not os.path.exists(args[0][value]): continue
                    f_.log_error('La ruta especificada debe no existir.')
                    return
            return f(f_, *args, **kwargs)
        return f2
    return fnct

class NekomukCommands(SyncTree):
    commands = set(['startproject', 'addpath', 'sync'])
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.log_error = logging.error
    
    def execute(self, command, args):
        if not command in self.commands:
            self.log_error('Método inválido')
            return
        getattr(self, 'command_%s' % command)(args)
    
    @required(min_args=1, not_valid_path=0)
    def command_startproject(self, args):
        shutil.copytree(os.path.join(NEKOMUK_DIR, 'share'), args[0])
        cprint(
            'El directorio "%s" se ha creado correctamente.' % args[0],
            'green'
        )
        print(
            'Ahora puede acceder al nuevo directorio y añadir directorios '\
            'para analizar mediante el comando "addpath".'
        )
    
    @required(min_args=1, valid_path=0)
    def command_addpath(self, args):
        infodevs = infodevice.InfoDevice()
        infodev = infodevs.get_device_by_path(args[0])
        if not infodev:
            parser.error(
                'La ruta establecida existe, pero no parece pertenecer a un '\
                'dispositivo montado.'
            )
        elem = etree.Element('device')
        if infodev['label']:
            print('Label detectado: %s' % infodev['label'])
            elem.attrib['label'] = infodev['label']
        else:
            print(
                'La partición del dispositivo para la ruta no parece tener'\
                ' un label, por lo que se ha recurrido a su UUID: %s' % \
                infodev['uuid']
            )
            elem.attrib['uuid'] = infodev['uuid']
        elem.attrib['path'] = args[0].replace(infodev['path'], '', 1)
        if elem.attrib['path'].endswith('/'):
            elem.attrib['path'] = elem.attrib['path'][:-1]
        if elem.attrib['path'].startswith('/'):
            elem.attrib['path'] = elem.attrib['path'][1:]
        self.cfg.findall('devices')[0].append(elem)
        self.writecfg()
    
    def writecfg(self):
        with open('config.xml', 'w') as f:
            f.write(etree.tostring(self.cfg, pretty_print=True))

        