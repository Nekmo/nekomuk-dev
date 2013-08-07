<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" 
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-
        transitional.dtd" 
        doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" indent="yes"/>
    <xsl:template match="/home">
        <xsl:variable name="root_level" select="root_level"/>
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es-ES" dir="ltr" lang="es-ES"> 
            <head profile="http://gmpg.org/xfn/11"> 
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
                <title id="title">Índice- Nekomuk</title>
                <script type="text/javascript" id="script">
                    root_level = '';
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/jquery.min.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/jquery.history.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/jquery.hoverIntent.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/jquery.cookie.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/jquery.slideto.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/jquery.hipster-titles.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/moment.min.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/moment.es.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/dir.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>static/js/home.js
                    </xsl:attribute>
                </script>
                <!--Escrito con Kate en entorno KDE4 bajo un sistema GNU/Linux (Distribución Archlinux) --> 
                <link type="text/css" rel="stylesheet"> 
                    <xsl:attribute name="href">
                        <xsl:value-of select="$root_level"/>static/css/dir.css
                    </xsl:attribute>
                </link>
                <link type="text/css" rel="stylesheet"> 
                    <xsl:attribute name="href">
                        <xsl:value-of select="$root_level"/>static/css/home.css
                    </xsl:attribute>
                </link>
                <link type="text/css" rel="stylesheet"> 
                    <xsl:attribute name="href">
                        <xsl:value-of select="$root_level"/>static/css/jquery.hipster-titles.css
                    </xsl:attribute>
                </link>
            </head> 
         
            <body>
                <div id="pattern">
                    <div class="file">
                        <span class="name"></span>
                    </div>
                    <div class="dir">
                        <a class="name" href=""></a>
                    </div>
                    <div class="result">
                        <a href="" class="device"><span></span><div class="divExtra"></div></a>
                        <span class="arrow first"></span>
                        <a href="" class="path"><span></span></a>
                        <a href="" class="name"><span></span></a>
                    </div>
                </div>
                <div id="top">
                    <div id="subtop">
                        <div id="search">
                            <input type="text" title="Comenzar búsqueda"  autocomplete="off" value="" />
                        </div>
                        <div id="exit_search" onClick="erase_input(this);">Salir del modo búsqueda</div>
                        <div id="start_search">
                            <div></div>
                            <span>Comience a escribir para buscar</span>
                        </div>
                    </div>
                </div>
                <div id="logo_div"></div>
                <div id="info_column_background">.</div>
                <div id="results" class="hide">
                    <div class="info_column">
                        <span class="device">
                            Dispositivo
                        </span>
                        <span class="path">
                            Ruta
                        </span>
                    </div>
                    <div class="files"></div>
                    <div class="info_search">
                        <div>
                            Se han encontrado <strong><span class="num"></span></strong> resultados buscando por <strong><span class="q"></span></strong>
                            <div class="tsun">¡N-no te vayas a pensar que los he encontrado por ti! ¡Tonto!</div>
                            <div class="divExtra"></div>
                        </div>
                    </div>
                    <div id="no_results">
                        <h1>¡N-no es que lo estuviese buscando por ti!</h1>
                        <span>
                            ...pero <strong>no he podido encontrar lo que buscabas</strong>. No te hagas una idea equivocada y vayas a pensar que quería encontrarlo, pero... ¿por qué no pruebas con otros términos?
                        </span>
                    </div>
                </div>
                <div id="content" class="view_list_details">
                    <div id="box">
                        <div class="option explore">
                            <div>
                                <div></div>
                            </div>
                            <span>Explorar</span>
                        </div>
                        <div class="option search">
                            <div>
                                <div></div>
                            </div>
                            <span>Buscar</span>
                        </div>
                        <div class="option collections">
                            <div>
                                <div></div>
                            </div>
                            <span>Colecciones</span>
                        </div>
                        <div class="option about">
                            <div>
                                <div></div>
                            </div>
                            <span>Acerca de</span>
                        </div>
                    </div>
                    <div id="more_info">
                        <div class="explore">
                            <span class="info">
                                Navegue por sus unidades de almacenamiento en cualquier momento y en cualquier lugar aunque estas no se encuentren disponibles. Obtenga detalles sobre sus archivos como tamaño, fecha de modificación, tipo, códecs, una previsualización o su suma de comprobación (MD5, SHA1, CRC32...).
                            </span>
                            <xsl:for-each select="devices/device">
                                <xsl:sort select="quote_name" /> 
                                <div class="device">
                                    <a class="name">
                                        <xsl:attribute name="href">devices/<xsl:value-of select="name_quote"/>/index.xml</xsl:attribute>
                                        <span class="method">
                                            <strong><xsl:value-of select="method" />:</strong>
                                            <xsl:value-of select="method_value" />
                                        </span>
                                        <span class="path">
                                            <xsl:value-of select="path" />
                                        </span>
                                    </a>
                                    <div class="data">
                                        En este dispositivo hay un total de <strong><xsl:value-of select="ndirs" /> directorios</strong> y <strong><xsl:value-of select="nfiles" /> archivos</strong>.
                                    </div>
                                </div>
                            </xsl:for-each>
                        </div>
                        <div class="search">
                            <span class="info">
                                Ahorre tiempo mediante búsquedas instantáneas en sus unidades de almacenamiento. Las búsquedas se realizan mediante mediante el sistema <i>full text search</i>, por lo que se tendrá en cuenta cualquier parte de la cadena del nombre del archivo o directorio.
                            </span>
                            <div class="data">
                                La búsqueda se realizará entre <strong><xsl:value-of select="total/ndirs" /> directorios</strong> y <strong><xsl:value-of select="total/nfiles" />  archivos</strong>.
                            </div>
                        </div>
                        <div class="collections">
                            <span class="info">
                                Organice sus archivos y directorios mediante colecciones para saberlo todo sobre ellos: duración total, estadísticas de códecs, clasificación por tags, por iconos...
                            </span>
                        </div>
                        <div class="about">
                            <span class="info">
                                Nekomuk es una aplicación de software libre ideado para aquellas personas con grandes cantidades de archivos multimedia, que requieren saber qué tienen almacenado, aunque no tengan acceso directo a los archivos (disco duro desconectado, en otro equipo...). Nekomuk no permite el acceso a los archivos, pero sí a varios de sus metadatos. Gracias a Nekomuk puede evitarse la duplicidad de archivos y saber dónde se encuentra almacenado un archivo.
                            </span>
                        </div>
                    </div>
                </div>
                <div id="divExtra01"></div>
                <div id="divExtra02"></div>
                <div id="divExtra03"></div>
                <div id="divExtra04"></div>
                <div id="divExtra05"></div>
                <div id="divExtra06"></div>
                <div id="divExtra07"></div>
                <div id="divExtra08"></div>
                <div id="divExtra09"></div>
                <div id="divExtra10"></div>
            </body> 
        </html>
    </xsl:template>
</xsl:stylesheet>