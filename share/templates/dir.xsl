<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" 
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-
        transitional.dtd" 
        doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" indent="yes"/>
    <xsl:template match="/dir">
        <xsl:variable name="root_level" select="root_level"/>
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es-ES" dir="ltr" lang="es-ES"> 
            <head profile="http://gmpg.org/xfn/11"> 
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
                <title id="title"><xsl:value-of select="name" /> - Nekomuk</title>
                <script type="text/javascript" id="script">
                    root_level = '../../<xsl:value-of select="$root_level" />';
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>../../static/js/jquery.min.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>../../static/js/jquery.history.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>../../static/js/jquery.hoverIntent.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>../../static/js/jquery.cookie.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>../../static/js/jquery.slideto.js
                    </xsl:attribute>
                </script>
                <script type="text/javascript">
                    <xsl:attribute name="src">
                        <xsl:value-of select="$root_level"/>../../static/js/main.js
                    </xsl:attribute>
                </script>
                <!--Escrito con Kate en entorno KDE4 bajo un sistema GNU/Linux (Distribución Archlinux) --> 
                <link type="text/css" rel="stylesheet"> 
                    <xsl:attribute name="href">
                        <xsl:value-of select="$root_level"/>../../static/css/style.css
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
                </div>
                <div id="top">
                    <div id="subtop">
                        <div id="search">
                            <input type="text" title="¿Qué desea buscar hoy?" />
                        </div>
                        <div>
                        </div>
                    </div>
                    <div id="view">
                        <span class="icons" title="Modo de Vista de iconos"></span>
                        <span class="details" title="Modo de vista detallada"></span>
                    </div>
                </div>
                <div id="logo_div"></div>
                <div id="panel">
                    <div id="thumb_wrapper">
                        <div id="frame_thumb">
                            <div id="thumb">
                            </div>
                            <div class="desc">Sin captura</div>
                        </div>
                    </div>
                    <div class="verbose">
                        <span class="container_text label">Contenedor</span>
                        <span class="container data"></span>
                    </div>
                    <div class="verbose">
                        <span class="size_text label">Tamaño</span>
                        <span class="size data"></span>
                    </div>
                    <div class="verbose">
                        <span class="length_text label">Duración</span>
                        <span class="length data"></span>
                    </div>
                    <div class="verbose">
                        <span class="video_codec_text label">Códec. vídeo</span>
                        <span class="video_codec data"></span>
                    </div>
                    <div class="verbose">
                        <span class="resolution_text label">Resolución</span>
                        <span class="resolution data"></span>
                    </div>
                    <div class="verbose">
                        <span class="aspect_text label">Rel. aspecto</span>
                        <span class="aspect data"></span>
                    </div>
                    <div class="verbose">
                        <span class="fps_text label">FPS</span>
                        <span class="fps data"></span>
                    </div>
                    <div class="verbose">
                        <span class="audio_codec_text label">Códec. audio</span>
                        <span class="audio_codec data"></span>
                    </div>
                    <div class="verbose">
                        <span class="samplerate_text label">Ratio audio</span>
                        <span class="samplerate data"></span>
                    </div>
                    <div class="verbose">
                        <span class="audio_channels_text label">Canales audio</span>
                        <span class="audio_channels data"></span>
                    </div>
                </div>
                <div id="results">
                    <div class="dirs">
                    </div>
                    <div class="files">
                    </div>
                </div>
                <div id="info_column_background">.</div>
                <div id="content" class="view_list_details">
                    <div class="files">
                        <div id="info_column">
                            <span class="name">
                                Nombre
                            </span>
                            <span class="size">
                                Tamaño
                            </span>
                            <span class="mean_size">
                                Tamaño medio
                            </span>
                        </div>
                        <div class="filediv dir">
                            <a href="../index.xml">
                                <img class="icon" alt="[Up]">
                                    <xsl:attribute name="src"><xsl:value-of select="$root_level"/>../../static/icons/go_up.svg</xsl:attribute>
                                </img>
                            </a>
                            <a href="../index.xml">..</a>
                            <span class="size">
                                <xsl:value-of select="human_size" />
                            </span>
                            <span class="mean_size">
                                <xsl:value-of select="human_mean_size" />
                            </span>
                        </div>
                        <!-- {% for subdir in dir.dirs|sort %} -->
                        <xsl:for-each select="dirs/dir">
                            <xsl:sort select="name" /> 
                            <div class="filediv dir">
                                <a>
                                    <xsl:attribute name="href"><xsl:value-of select="url"/>/index.xml</xsl:attribute>
                                    <img class="icon" alt="[Dir]">
                                        <xsl:attribute name="src"><xsl:value-of select="$root_level" />../../static/icons/<xsl:value-of select="icon" /></xsl:attribute>
                                    </img>
                                </a>
                                <a>
                                    <xsl:attribute name="href"><xsl:value-of select="quote_name"/>/index.xml</xsl:attribute>
                                    <xsl:value-of select="name" />
                                </a>
                                <span class="size">
                                    <xsl:value-of select="human_size" />
                                </span>
                                <span class="mean_size">
                                    <xsl:value-of select="human_mean_size" />
                                </span>
                            </div>
                        </xsl:for-each>
                        <!-- {% endfor %} -->
                        <!-- {% for subfile in dir.files|sort %} -->
                        <xsl:for-each select="files/file">
                            <div class="filediv file">
                                <img class="icon" alt="[*]" src="{{ root_level }}static/icons/{{ subfile.get_icon() }}">
                                    <xsl:attribute name="src"><xsl:value-of select="$root_level"/>../../static/icons/<xsl:value-of select="icon" /></xsl:attribute>
                                </img>
                                <span class="name">
                                    <xsl:value-of select="name" />
                                </span>
                                <span class="width verbose">
                                    <xsl:value-of select="metadata/videos/video[1]/width" />
                                </span>
                                <span class="height verbose">
                                    <xsl:value-of select="metadata/videos/video[1]/height" />
                                </span>
                                <span class="container verbose">
                                    <xsl:value-of select="metadata/type" />
                                </span>
                                <span class="length verbose">
                                    <xsl:value-of select="metadata/length" />
                                </span>
                                <span class="thumb verbose">
                                    <xsl:value-of select="thumb" />
                                </span>
                                <span class="video_codec verbose">
                                    <xsl:value-of select="metadata/videos/video[1]/codec" />
                                </span>
                                <span class="audio_codec verbose">
                                    <xsl:value-of select="metadata/audios/audio[1]/codec" />
                                </span>
                                <span class="aspect verbose">
                                    <xsl:choose>
                                        <xsl:when test="metadata/videos/video[1]/aspect &gt; 1.6 and metadata/videos/video[1]/aspect &lt; 1.8">
                                            16:9
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="metadata/videos/video[1]/aspect" />
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </span>
                                <span class="fps verbose">
                                    <xsl:choose>
                                        <xsl:when test="metadata/videos/video[1]/fps &gt; 23.6">
                                            24
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="metadata/videos/video[1]/fps" />
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </span>
                                <span class="samplerate verbose">
                                    <xsl:value-of select="metadata/audios/audio[1]/samplerate" />
                                </span>
                                <span class="audio_channels verbose">
                                    <xsl:value-of select="metadata/audios/audio[1]/channels" />
                                </span>
                                <span class="size">
                                    <xsl:value-of select="human_size" />
                                </span>
                            </div>
                        <!-- {% endfor %} -->
                        </xsl:for-each>
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