# -*- coding: utf-8 -*-
import os
import re
import shutil

import sys

try:
    from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
    from PyKDE4.kdeui import KApplication
    from PyKDE4.kdeui import KIcon
    from PyQt4.QtCore import QSize
except:
    pykde_available = False
else: 
    appName     = "KApplication"
    catalog     = ""
    programName = ki18n ("KApplication")
    version     = "1.0"
    description = ki18n ("KApplication/KMainWindow/KAboutData example")
    license     = KAboutData.License_GPL
    copyright   = ki18n ("(c) 2007 Jim Bublitz")
    text        = ki18n ("none")
    homePage    = "www.riverbankcomputing.com"
    bugEmail    = "jbublitz@nwinternet.com"
     
    aboutData   = KAboutData (appName, catalog, programName, version, description,
                            license, copyright, text, homePage, bugEmail)
     
    KCmdLineArgs.init (sys.argv[:1], aboutData)
     
    app = KApplication()
    pykde_available = True

class GetIcon(object):
    def detect_dir_icon(self, root):
        """Detectar si el directorio tiene un icono, y si es afirmativo, devolver
        la ruta del mismo.
        """
        if not os.path.exists(root):
            return False
        # KDE
        if '.directory' in os.listdir(root):
            # .directory es un archivo de meta-datos que se encuentra dentro del
            # directorio con información sobre el mismo, uno de los datos posibles
            # es el icono.
            data = open(os.path.join(root, '.directory')).read()
            icon = re.findall('Icon=(.+)', data, re.MULTILINE)
            if not icon:
                return False
            icon = icon[0]

            if not icon.startswith('/') and pykde_available:
                # El icono no es una ruta al icono, sino el nombre del mismo, y se
                # necesita obtener del directorio del tema de iconos del sistema.
                if not KIcon.hasThemeIcon(icon):
                    return False
                theme = str(KIcon.themeName())
                path = '/tmp/%s:%s.png' % (theme, icon)
                if not os.path.exists(path):
                    KIcon(icon).pixmap(QSize(64,64)).save(path)
                return path
            if not icon.startswith('/') and not pykde_available:
                # Es como el caso anterior un nombre del icono, pero no se posee
                # el directorio de iconos, por lo que el proceso fallará
                return False
            else:
                # Es una ruta al icono, se devuelve
                return icon
        return False