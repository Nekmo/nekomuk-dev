#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Nekomuk, un gestor de archivos multimedia, estén disponibles o no.
"""
import os
import sys
from lxml import etree
import logging
import argparse
# sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import nekomuk

log_metadata = logging.getLogger('metadata')
log_metadata.setLevel(logging.CRITICAL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--debug', dest='loglevel', action='store_const',
                        const=logging.DEBUG, default=logging.INFO,
                        help='Establecer el nivel de los logs a debug.')
    parser.add_argument('--warning', dest='loglevel', action='store_const',
                        const=logging.WARNING, default=logging.INFO,
                        help='Establecer el nivel de los logs a solo advertencias.')
    parser.add_argument('--error', dest='loglevel', action='store_const',
                        const=logging.ERROR, default=logging.INFO,
                        help='Establecer el nivel a solo errores del programa.')
    parser.add_argument('mode', choices=nekomuk.NekomukCommands.commands,
                        help='Modo de uso')
    parser.add_argument('extra_args', nargs='*')
    args = parser.parse_args()
    logger = logging.getLogger('nekomuk')
    logger.setLevel(args.loglevel)
    #ch = logging.StreamHandler()
    #ch.setLevel(args.loglevel)
    #ch.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    #logger.addHandler(ch)

    if not os.path.exists('config.xml') and not args.mode == 'startproject':
        parser.error(
            'El directorio actual no parece ser un proyecto válido. Abortando.'
        )
    elif args.mode == 'startproject':
        root = None
    else:
        root = etree.parse('config.xml').getroot()
    nekomukcommands = nekomuk.NekomukCommands(root)
    nekomukcommands.log_error = parser.error
    nekomukcommands.execute(args.mode, args.extra_args)