# -*- coding: utf-8 -*-
import asyncore
import socket
import io
import sys
import logging
import mimetypes
import os

import mimetypes
mimetypes.init()

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf8')
    from urllib import unquote, quote
else:
    from urllib.parse import unquote, quote

from . import ioserver

HTTP_VER = 'HTTP/1.1'
WEBSOCKET_MAGIC_KEY = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

HTTP_RESPONSES = {
    101: 'Switching Protocols',
    200: 'OK',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Internal Server Error',
}

SERVER_MSG = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>%(code)i %(msg_code)s</title>
</head><body>
<h1>%(code)i: %(msg_code)s</h1>
<hr>
<address>NekHTTP.</address>
</body></html>"""

pypaths_exact = [
    
]

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

pypaths_startswith = [
    ('/io.py', {'method': 'fnct', 'fnct': ioserver.IORequest().get}),
    ('', {'method': 'static_dir', 'path': os.getcwd()}),
]

pypaths_regex = [
]

class HTTPRequest(object):
    code = 200
    msg_code = ''
    charset = 'UTF-8'
    body = ''
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.resp_headers = {
            'Server': 'NekHTTP',
        }
    
    def submit_file(self, path, mime=False):
        if not mime:
            mime = mimetypes.guess_type(path)[0]
            if not mime: mime = 'text/plain'
            if mime.startswith('text/'):
                mime += '; charset=%s' % self.charset
        self.set_header('Content-Type', mime)
        if not os.path.exists(path):
            self.return_error(404)
            return
        file_stats = os.stat(path)
        self.set_header('Content-Length', str(file_stats.st_size))
        self.set_header('ETag', str(int(file_stats.st_mtime)))
        self.body = open(path, 'rb')
        self.send()
        
    def set_header(self, key, val):
        self.resp_headers[key] = val

    def del_header(self, key):
        del self.resp_headers[key]
        
    def send(self, body=None, mime='text/html'):
        if body:
            self.body = body
        if self.main.protocol == 'websockets':
            len_body = len(self.body)
            if len_body < 126:
                # Mensaje pequeño, único caracter de longitud.
                sum_body = chr(len_body)
            elif len_body < 256:
                # Mensaje mediano. Menor a 256, pero con 3 caracteres.
                sum_body = '\x7e\x00' + chr(len_body)
            else:
                # Mensaje grande, se usan los 2 caracteres de longitud.
                sum_body = '\x7e' + self.dump_big_endian(len_body)
            self.body = '\x81' + sum_body  + self.body
            self.main.send(self.body)
            return
        if self.body and not 'Content-Type' in self.resp_headers.keys():
            self.set_header('Content-Type', mime)
        if self.body and not 'Content-Length' in self.resp_headers.keys():
            if isinstance(self.body, unicode):
                self.body = self.body.encode('utf-8')
            self.set_header('Content-Length', len(self.body))
        if not self.msg_code:
            self.msg_code = HTTP_RESPONSES.get(self.code, 'Code %i' % self.code)
        # Se añade código de respuesta
        resp = '%s %i %s\r\n' % (HTTP_VER, self.code, self.msg_code)
        # Se añaden los headers
        for key, value in self.resp_headers.items():
            resp += '%s: %s\r\n' % (key, value)
        # Se añade el body
        resp += '\r\n'
        if 'read' in dir(self.body):
            self.main.send(resp)
            while True:
                data = self.body.read(2048)
                if not data:
                    break
                self.main.send(data)
        else:
            if 'Sec-WebSocket-Accept' in self.resp_headers.keys():
                #resp = resp[:-2]
                self.main.send(resp)
                return
            self.main.send(resp)
            #bodyIO = StringIO(self.body)
            #while True:
                #data = bodyIO.read(2048)
                #if not data: break
                #self.main.send(data)
            self.main.send(self.body)
        #self.main.close()
    
    def start_websocket(self, fnct, protocol='NekProtocol'):
        #print(self.headers)
        if self.headers.get('Upgrade', False) != 'websocket':
            raise WebsocketError
        sec_key = self.headers['Sec-WebSocket-Key']
        digest = sha1(sec_key + WEBSOCKET_MAGIC_KEY).digest()
        sec_accept = base64.b64encode(digest)
        self.del_header('Server')
        self.set_header('Sec-WebSocket-Accept', sec_accept)
        self.set_header('Sec-WebSocket-Protocol', protocol)
        self.set_header('Upgrade', 'websocket')
        self.set_header('Connection', 'Upgrade')
        self.code = 101
        self.send()
        self.main.protocol = 'websockets'
        self.main.ws_fnct = fnct
    
    def return_error(self, code):
        self.code = code
        self.set_header('Content-Type', 'text/html')
        self.msg_code = HTTP_RESPONSES.get(code, 'Number error: %i' % code)
        self.body = SERVER_MSG % {'code': code, 'msg_code': self.msg_code}
        self.send()
        self.main.close()

    def dump_big_endian(self, n):
        s = '%x' % n
        if len(s) & 1:
            s = '0' + s
        return s.decode('hex')

    def jinja_resp(self, filename, args={}, env='default', code=200):
        self.code = code
        env = jinja_envs[env]
        template = env.get_template(filename)
        self.body = template.render(args)
        self.send()
        
        
class ServerHandler(asyncore.dispatcher_with_send):
    protocol = 'http' # El protocolo define si es http o websocket
    valid_pypath_methods = ['static_dir', 'fnct']
    def handle_read(self):
        data = self.recv(8192)
        if not data:
            return
        if self.protocol == 'http':
            self.parse_http(data)
        elif self.protocol == 'websockets':
            self.ws_fnct(self.decode_websockets(data))
            
        #self.send('!!\n')
    
    def parse_http(self, data):
        """ Obtener los datos de una petición HTTP
        """
        # ex. GET archivo?key=value HTTP/1.1
        # Se parsea la primera línea
        first_line = data.split('\n', 1)[0]
        first_line_split = first_line.split(' ')
        method = first_line_split[0] # GET, POST...
        path = first_line_split[1] # archivo?key=value
        http_ver = first_line_split[2] # ex. HTTP/1.1
        del first_line_split
        path_split = path.split('?', 1) # ['archivo', 'key=value']
        if len(path_split) > 1:
            get_args = self.split_quote(path_split[1])
        else:
            get_args = {}
        path = path_split[0] # archivo
        path = path.replace('../', '') # Medida de seguridad
        path = unquote(path)
        del path_split
        # Parsear los headers
        headers = {}
        # TODO (sumando +1 o +2 dependiendo de FF o Chromium)
        #print(repr(data))
        bytesbuffer = io.BytesIO(data[len(first_line) + 1:])
        while True:
            line = bytesbuffer.readline()[:-2]
            if line:
                line_split = line.split(': ', 1)
                headers[line_split[0]] = line_split[1]
            else:
                break
        # Leer el resto del documento (POST)
        if method == 'POST':
            post = self.split_quote(bytesbuffer.read())
        else:
            post = []
        
        request = HTTPRequest(**{
            'method': method,
            'path': path,
            'http_ver': http_ver,
            'headers': headers,
            'post': post,
            'get': get_args,
            '_send': self.send,
            'main': self,
        })
        # Determinar qué cargar por el path
        for pypath in pypaths_exact:
            if pypath[0] == path:
                self.load_pypath(request, pypath)
                return
        # TODO poner delante pypaths_startswith
        for pypath in pypaths_regex:
            groups = re.findall(pypath[0], path)
            if groups:
                request.groups = groups[0]
                self.load_pypath(request, pypath)
                return
        for pypath in pypaths_startswith:
            if request.path.startswith(pypath[0]):
                self.load_pypath(request, pypath)
                return
    
    def load_pypath(self, request, pypath):
        if not pypath[1]['method'] in self.valid_pypath_methods:
            request.return_error(500)
            logging.error('Pypath method desconocido: %s' % pypath[1]['method'])
            return
        fnct = getattr(self, 'load_pypath_' + pypath[1]['method'])
        fnct(request, pypath)
    
    def load_pypath_static_dir(self, request, pypath):
        path = os.path.join(pypath[1]['path'], request.path[1:])
        path = path.replace(pypath[0], '', 1)
        if os.path.isdir(path):
            path = os.path.join(path, 'index.xml')
            if not os.path.exists(path):
                request.return_error(403)
                return
        request.submit_file(path)

    def load_pypath_fnct(self, request, pypath):
        pypath[1]['fnct'](request, pypath)
            
    def split_quote(self, txt):
        """Dividir un string "key=val&key2=val2" en un diccionario
        """
        result = {}
        for pair in txt.split('&'):
            key, value = pair.split('=')
            if not key in result:
                result[key] = []
            result[key].append(value)
        return result

        
    def decode_websockets(self, stringstreamin):
        #turn string values into opererable numeric byte values
        # Author: http://stackoverflow.com/a/9778823/528597
        byteArray = [ord(character) for character in stringstreamin]
        datalength = byteArray[1] & 127
        indexFirstMask = 2 
        if datalength == 126:
            indexFirstMask = 4
        elif datalength == 127:
            indexFirstMask = 10
        masks = [m for m in byteArray[indexFirstMask : indexFirstMask+4]]
        indexFirstDataByte = indexFirstMask + 4
        decodedChars = []
        i = indexFirstDataByte
        j = 0
        while i < len(byteArray):
            decodedChars.append( chr(byteArray[i] ^ masks[j % 4]) )
            i += 1
            j += 1
        decodedChars = ''.join(decodedChars)
        return decodedChars


class HTTPServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(10)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = ServerHandler(sock)