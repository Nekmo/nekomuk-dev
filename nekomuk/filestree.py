#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import mimetypes
import shutil

import os
import re

import sys
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf8')

from kaa import metadata
import kaa.metadata.video.core
import kaa.metadata.audio.core
from lxml import etree

if sys.version_info < (3,0):
    import urllib as parse
else:
    from urllib import parse

from . import render
from . import thumb
from . import get_icon

setattr(kaa.metadata.video.core.AVContainer, 'interfaces',
    ['audio', 'video', 'subtitles', 'type', 'length'])
setattr(kaa.metadata.video.core.VideoStream, 'interfaces', 
    ['codec', 'width', 'height', 'aspect', 'fps']
)
setattr(kaa.metadata.audio.core.Audio, 'interfaces',
    ['codec', 'samplerate', 'channels']
)
setattr(kaa.metadata.video.core.Subtitle, 'interfaces',
    ['language', 'title']
)
    
class RenderXML(object):
    interfaces = set()
    _ignore_in_parent = set()
    _xml_structure = {'name': 'root', 'sub': {}}

    def build_xml(self, isroot=True, path=None):
        self._render_path = path
        def render_element(name, obj, parent, structure):
            if structure['name']:
                element = etree.SubElement(parent, structure['name'])
            else:
                element = etree.SubElement(parent, name)
            if isinstance(obj, (list, tuple, set)):
                if not structure['name'] and not name.endswith('s'):
                    element.tag = name + 's'
                if not 'sub' in structure:
                    substructure = {'name': None}
                else:
                    substructure = structure['sub']
                for subelement in obj:
                    render_element(name, subelement, element, substructure)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    if structure.get('sub', False) and key in structure['sub']:
                        substructure = structure['sub'][key]
                    else:
                        substructure = {'name': None}
                    render_element(key, value, element, substructure)
            elif isinstance(obj, kaa.metadata.core.Media):
                for key in obj.keys():
                    if 'interfaces' in dir(obj) and not key in obj.interfaces:
                        continue
                    value = obj[key]
                    if structure.get('sub', False) and key in structure['sub']:
                        substructure = structure['sub'][key]
                    else:
                        substructure = {'name': None}
                    render_element(key, value, element, substructure)
            elif isinstance(obj, RenderXML):
                if not structure['name'] and obj._xml_structure['name']:
                    element.tag = obj._xml_structure['name']
                for subelement in obj.build_xml(False, path):
                    element.append(subelement)
            else:
                element.text = unicode(str(obj))
            return element
        root = etree.Element(self._xml_structure['name'])
        for interface in self.interfaces:
            if not isroot and interface in self._ignore_in_parent:
                continue
            render_element(
                interface, getattr(self, interface), root,
                self._xml_structure['sub'].get(interface, {'name': None})
            )
        return root

    def render(self, path, stylesheet, name='index'):
        root = self.build_xml(path=path)
        if path.endswith(os.sep):
            path = path[:-1]
        if not path:
            stylesheet_path = 'templates/' + stylesheet
        else:
            stylesheet_path = os.path.join(
                '../' * len(path.split(os.sep)),
                'templates/',
                 stylesheet
            )
        pi = etree.PI(
            'xml-stylesheet type="text/xsl" href="%s"' % stylesheet_path
        )
        root.addprevious(pi)
        tree = etree.ElementTree(root)
        tree.write(os.path.join(path, name + '.xml'),
            pretty_print=True,
            encoding='UTF-8',
            xml_declaration='1.0'
        )
        render.write_render(root, os.path.join(path, name + '.html'), stylesheet)        


class Path(RenderXML):
    def __init__(self, *args):
        self.root, self.relative_root, self.name, self.tree = args
        self.quote_name = parse.quote_plus(self.name)
        self.complete_path = os.path.join(self.root, self.relative_root)
        # Intentar conocer el directorio padre
        root_split = self.relative_root.split(os.sep)
        relative_parent_root = os.sep.join(root_split[:-1])
        if len(root_split) > 1:
            if not relative_parent_root in self.tree.paths:
                # Se crea instancia para el directorio padre
                self.parent = self.dir_class(
                    self.root,
                    relative_parent_root,
                    self.root_split[-2],
                    self.tree
                )
                self.tree.paths[parentobj.relative_root] = self.parent
            else:
                self.parent = self.tree.paths[relative_parent_root]
        elif len(root_split) == 1 and self.name:
            self.parent = self.tree.paths['']
        else:
            self.parent = None

    def __lt__(self, other):
        return self.name < other.name
    
    def __gt__(self, other):
        return self.name > other.name
    
    def __le__(self, other):
        return self.name <= other.name
    
    def __ge__(self, other):
        return self.name >= other.name

class Dir(Path, get_icon.GetIcon):
    _xml_structure = {
        'name': 'dir',
        'sub': {
            'path_dirs': {
                'name': 'path_dirs',
                'sub': {
                    'name': 'dirname',
                }
            }
        }
    }
    interfaces = set((
        'name', 'size', 'files', 'dirs', 'root_level', 'quote_name',
        'human_size', 'human_mean_size', 'mean_size', 'icon', 'mtime',
        'quote_device', 'device_name', 'path_dirs', 'filetype'
    ))
    _ignore_in_parent =set((
        'files','dirs', 'root_level', 'device_name', 'quote_device',
        'path_dirs'
    ))
    last_render = None
    filetype = 'dir'

    def __init__(self, root, relative_root, name, tree):
        self.dirs = []
        self._dirs_names = []
        self.files = []
        self.size = 0
        self.sub_size = 0
        self.mtime = 0
        self.sub_mtime = 0
        self.update_required = False
        Path.__init__(self, root, relative_root, name, tree)
        self.relative_level = len(self.relative_root.split(os.sep))
        if not self.relative_root:
            self.relative_level -= 1
        self.root_level = '../' * self.relative_level
        
    def append_dir(self, subdirobj):
        self._dirs_names
        self.dirs.append(subdirobj)
    
    def append_file(self, subfileobj):
        self.files.append(subfileobj)
        
    @property
    def human_size(self):
        return render.humanize(self.size)

    @property
    def quote_device(self):
        return parse.quote(self.tree.device.quote_name)

    @property
    def device_name(self):
        return parse.unquote(self.tree.device.quote_name)

    @property
    def path_dirs(self):
        return self.relative_root.split(os.sep)

    def __str__(self, level=0):
        body = ' ' * level
        file_indent = ' ' * (level + 2)
        body += '|- %s\n' % self.name
        for dir in self.dirs:
            body += dir.__str__(level + 2)
        for file in self.files:
            body += '%s%s\n' % (file_indent, file.name)
        return body
        
    def add_size(self, size, is_parent=True):
        self.size += size
        if is_parent:
            self.sub_size += size
        if self.parent:
            self.parent.add_size(size, False)

    def add_mtime(self, mtime, is_parent=True):
        if mtime > self.mtime:
            self.mtime = mtime
        if is_parent and mtime > self.sub_mtime:
            self.sub_mtime = mtime
        if self.parent:
            self.parent.add_mtime(mtime, False)

    @property
    def mean_size(self):
        return self.get_mean_size()

    @property
    def human_mean_size(self):
        return render.humanize(self.mean_size)

    def get_mean_size(self):
        nsizes = len(self.files)
        if not nsizes: return 0
        return self.sub_size / (nsizes * 1.0)
        
    @property
    def icon(self):
        icon = self.detect_dir_icon(self.complete_path)
        if not icon:
            return 'folder.svg'
        quote_icon = parse.quote_plus(icon)
        project_icon = os.path.join('static/icons', quote_icon)
        if not os.path.exists(project_icon):
            shutil.copy(icon, project_icon)
        return parse.quote(quote_icon)


    def render(self, path):
        if not self.last_render is None:
            # Comprobar si el icono del directorio ha cambiado. Si es así, forzar upd.
            if self.last_render.find('icon').text != self.icon:
                self.update_required = True
                if self.parent:
                    self.parent.update_required = True
                    self.parent.render(os.path.dirname(path))
        if not self.last_render is None and not self.update_required:
            if (int(float(self.last_render.find('mtime').text)) == int(self.mtime) and 
                    int(float(self.last_render.find('size').text)) == int(self.size)):
                return
        if not self.last_render is None:
            # Comprobar si hay directorios que ya no deben existir en el proyecto
            for dir in os.walk(path).next()[1]:
                if dir in self._dirs_names: continue
                shutil.rmtree(os.path.join(path, dir))
        level = '../' * self.relative_level
        root = self.build_xml(path=path)
        stylesheet = "../../%stemplates/dir.xsl" % ('../' * self.relative_level)
        pi = etree.PI(
            'xml-stylesheet type="text/xsl" href="%s"' % stylesheet
        )
        root.addprevious(pi)
        tree = etree.ElementTree(root)
        tree.write(os.path.join(path, 'index.xml'),
            pretty_print=True,
            encoding='UTF-8',
            xml_declaration='1.0'
        )
        render.write_render(root, os.path.join(path, 'index.html'))        
            
    def __repr__(self):
        return '<Dir "%s">' % self.relative_root
        
class File(Path):
    _xml_structure = {'name': 'file', 'sub': {}}

    def __init__(self, root, relative_root, name, tree):
        Path.__init__(self, root, relative_root, name, tree)
        self.size = os.path.getsize(self.complete_path)
        self.human_size = render.humanize(self.size)
        self.mtime = os.path.getmtime(self.complete_path)
        self.relative_level = len(self.relative_root.split(os.sep)) - 1
        self.mimetype = mimetypes.guess_type(self.name)[0]
        if self.mimetype:
            self.filetype = self.mimetype.split('/')[0]
        else:
            self.filetype = None
        self.metadata = None
        if self.parent:
            self.parent.add_size(self.size)
            self.parent.add_mtime(self.mtime)

    @property
    def interfaces(self):
        if not self.metadata:
            self.get_metadata()
        return [
            'size', 'mtime', 'relative_level', 'filetype', 'name', 'metadata',
            'human_size', 'quote_name', 'icon', 'thumb',
        ]

    def __repr__(self):
        return '<Name "%s">' % self.name
    
    @property
    def thumb(self):
        if not self.filetype == 'video':
            return '0'
        to = os.path.join(self._render_path, self.name + '.jpg')
        if os.path.exists(to) and not self.parent.last_render is None:
            xpath = './/file[name/text() = "%s"]' % self.name
            file = self.parent.last_render.xpath(xpath)[0]
            if int(float(file.find('mtime').text) == int(self.mtime)):
                return '1'
        if not thumb.video_thumb(self.complete_path, to, (171, 96)):
            return '1'
        else:
            return '0'

    @property
    def icon(self):
        return '%s.svg' % self.filetype
    
    def get_metadata(self):
        try:
            self.metadata = metadata.parse(self.complete_path)
        except:
            self.metadata = {}
        # if self.metadata is None:
        #     self.metadata = {'video': False, 'audio': False}
        # if not self.metadata['video']:
        #     self.metadata['video'] = {}
        # else:
        #     self.metadata['video'] = self.metadata['video'][0]
        #     self.filetype = 'video'
        # if not self.metadata['audio']:
        #     self.metadata['audio'] = {}
        # else:
        #     self.metadata['audio'] = self.metadata['audio'][0]
        # if self.metadata[0]['video']:
        #     self.filetype = 'video'
        # elif self.metadata[0]['audio'] and not self.metadata[0]['video']:
        #     self.filetype = 'audio'
    
    def __getitem__(self, value):
        if not self.metadata: self.get_metadata()
        if value in self.metadata:
            return self.metadata[value]
        if value in self.interfaces:
            return getattr(self, value)
        raise KeyError('%s is not a valid method' % value)

class Tree(Dir):
    def __init__(self, root, dir_class=Dir, file_class=File, 
                dirsfilter=None, filesfilter=None, device=None):
        """
        """
        self.relative_root = ''
        self.relative_level = 0
        self.name = ''
        self.size = 0
        self.paths = {}
        self.dir_class = dir_class
        self.file_class = file_class
        self.device = device
        
        for dir_root, subdirs, subfiles in os.walk(root):
            relative_root = dir_root.replace(root, '', 1)[1:]
            relative = os.path.dirname(dir_root)
            dir_root_name = relative_root.split(os.sep)[-1]
            # root -> Dispositivo en que se está analizando (/media/device).
            # dir_root -> Directorio en análisis (/media/device/sub/folder).
            # dir_root_name -> nombre del directorio actual (folder).
            # relative_root -> dir_root relativo (sub/folder).
            # relative -> relative_root sin directorio actual
            # subdirs -> carpetas en el directorio dir_root
            # files -> Archivos en el directorio dir_root
            valid_dir = True
            # Comprobar si el directorio actual debe analizarse
            if dirsfilter and not dirsfilter.match(root, relative, dir_root_name):
                continue
            # Si es un directorio conocido, se usa el objeto para el directorio
            # existente. De lo contrario se crea.
            if relative_root in self.paths:
                dirobj = self.paths[relative_root]
            else:
                dirobj = dir_class(root, relative_root, dir_root_name, self)
                self.paths[relative_root] = dirobj
                if not dir_root_name:
                    self._dirobj = dirobj
                    self.dirs = self._dirobj.dirs
                    self.files = self._dirobj.files
            for subdir in subdirs:
                # Comprobar si el subdirectorio debe listarse o no.
                valid_dir = True
                if dirsfilter and not dirsfilter.match(root, relative_root, subdir):
                    subdirs.remove(subdir)
                    continue
                # Si es un subdirectorio conocido, se reutiliza el objeto.
                relative_subdir = os.path.join(relative_root, subdir)
                if relative_subdir in self.paths:
                    subdirobj = self.paths[relative_subdir]
                else:
                    subdirobj = dir_class(root, relative_subdir, subdir, self)
                    self.paths[relative_subdir] = subdirobj
                # Se añade el subdirectorio al directorio actual
                dirobj.append_dir(subdirobj)
            for subfile in subfiles:
                # Comprobar si el subarchivo debe listarse o no.
                if filesfilter and not filesfilter.match(root, relative_root, subfile):
                    continue
                # Se añade el subarchivo al directorio actual
                relative_subfile = os.path.join(relative_root, subfile)
                if not os.path.exists(os.path.join(dir_root, subfile)):
                    continue
                subfileobj = file_class(root, relative_subfile, subfile, self)
                dirobj.append_file(subfileobj)