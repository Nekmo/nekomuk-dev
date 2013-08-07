<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es-ES" dir="ltr" lang="es-ES"> 
    <head profile="http://gmpg.org/xfn/11"> 
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
        <title>{{ title }} - Nekomuk</title>
        <script type="text/javascript" src="{{ root_level }}static/js/jquery.min.js"></script>
        <script type="text/javascript" src="{{ root_level }}static/js/jquery.history.js"></script>
        <script type="text/javascript" src="{{ root_level }}static/js/jquery.hoverIntent.js"></script>
        <script type="text/javascript" src="{{ root_level }}static/js/jquery.cookie.js"></script>
        <script type="text/javascript" src="{{ root_level }}static/js/jquery.slideto.js"></script>
        <script type="text/javascript" src="{{ root_level }}static/js/main.js"></script>
        <script type="text/javascript">
        $(document.body).ready(function (){
        });
        </script>
        <!--Escrito con Kate en entorno KDE4 bajo un sistema GNU/Linux (Distribución Archlinux) --> 
        <link type="text/css" rel="stylesheet" href="{{ root_level }}static/css/style.css" /> 
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
                    <input type="text" title="&#191;Qu&#233; desea buscar hoy?" />
                </div>
                <div>
                    <span class="show_advance">Avanzado</span>
                    <div class="advance">
                        <div>
                            <input checked="checked" type="radio" name="advance" value="1" id="search_1"></input>
                            <label for="search_1">S&#243;lo aqu&#237;</label>
                        </div>
                    </div>
                    <div>
                        <input title="title" type="radio" name="advance" value="2" id="search_2"></input>
                        <label for="search_2">Dispositivo</label>
                    </div>
                    <div>
                        <input title="title" type="radio" name="advance" value="3" id="search_3"></input>
                        <label for="search_3">Todos los dispositivos</label>
                    </div>
                </div>
            </div>
            <div id="view">
                <span class="icons" title="Modo de Vista de iconos"></span>
                <span class="details" title="Modo de vista detallada"></span>
            </div>
        </div>
        <div id="logo_div"></div>
        <div id="panel">
            <div class="frame_thumb">
                <div class="left"></div>
                <div id="thumb"></div>
                <div class="right"></div>
            </div>
            <div class="verbose">
                <span class="container_text label"></span>
                <span class="container data"></span>
            </div>
            <div class="verbose">
                <span class="size_text label"></span>
                <span class="size data"></span>
            </div>
            <div class="verbose">
                <span class="length_text label"></span>
                <span class="length data"></span>
            </div>
            <div class="verbose">
                <span class="video_codec_text label"></span>
                <span class="video_codec data"></span>
            </div>
            <div class="verbose">
                <span class="resolution_text label"></span>
                <span class="resolution data"></span>
            </div>
            <div class="verbose">
                <span class="aspect_text label"></span>
                <span class="aspect data"></span>
            </div>
            <div class="verbose">
                <span class="fps_text label"></span>
                <span class="fps data"></span>
            </div>
            <div class="verbose">
                <span class="audio_codec_text label"></span>
                <span class="audio_codec data"></span>
            </div>
            <div class="verbose">
                <span class="samplerate_text label"></span>
                <span class="samplerate data"></span>
            </div>
            <div class="verbose">
                <span class="audio_channels_text label"></span>
                <span class="audio_channels data"></span>
            </div>
        </div>
        <div id="results">
            <div class="dirs">
            </div>
            <div class="files">
            </div>
        </div>
        <div id="content" class="view_list_details">
            {% block content %}{% endblock %}
        </div>
    </body> 
</html> 
