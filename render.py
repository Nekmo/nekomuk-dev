#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# from jinja2 import Environment, PackageLoader
import codecs
import os
from lxml import etree


sizes = {'b': 1, 'B': 8, 'KiB': 1024, 'MiB': 1048576.0, 'GiB': 1073741824.0}

def humanize(num):
    """Pasar el tamaño en bytes, a un string legible 'para humanos'"""
    def get_float(num, size):
        if round(num / size, 1) == num // size:
            num = int(num // size)
        else:
            num = round(num / size, 1)
        return num
    for size in sizes.keys():
        if num / 1024 >  sizes[size]:
            pass
        else:
            num = get_float(num, sizes[size])
            return '%s %s' % (num, size)
    # No se encuentra dentro de los rangos, se usa el último visto
    num = get_float(num, sizes[size])
    return '%s %s' % (num, size)

#jinja_env = Environment(loader=PackageLoader('nekomuk', 'templates'))
#jinja_env.filters['humanize'] = humanize

# def render(page='base.html', args={}):
#     template = jinja_env.get_template(page)
#     return template.render(**args)

def build_render(path):
    with open(path) as f:
        xslt_root = etree.XML(f.read())
    return etree.XSLT(xslt_root)


xsl_renders = {
    'dirs.xsl': build_render(os.path.join('templates', 'dir.xsl')),
}

def write_render(root, to_path, page='dirs.xsl'):
     with codecs.open(to_path, 'wb', 'utf-8') as f:
        f.write(unicode(xsl_renders['dirs.xsl'](root)))