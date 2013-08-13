$(document).ready(function(){
    // Poner moment en español
    moment.lang('es');

    String.prototype.startswith = function(str){
        return this.indexOf(str) == 0;
    };
    
    String.prototype.endswith = function(suffix) {
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    };

    Array.prototype.append = function (val){
        this[this.length] = val;
    };

    function safe_tags_replace(str) {
        function replaceTag(tag) {
            var tagsToReplace = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;'
            };
            return tagsToReplace[tag] || tag;
        }
        return str.replace(/[&<>]/g, replaceTag);
    }

    function escapeRegExp(str) {
      return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
    }

    complete_url = function(url, root){
        var new_url =  window.location.href;
        new_url = new_url.split('/').slice(0, -1).join('/') + '/';
        if(root == undefined || root == true){
            new_url = new_url + root_level + url;
        } else {
            new_url = new_url + url;
        }
        return new_url
    }

    xsltTransform = function(xmlfile, xslfile, onready) {
        var xmlhttp = new XMLHttpRequest();
        var xml, xslt;
        output = '';
        xmlhttp.open("get",xmlfile,false);
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                xml = xmlhttp.responseXML;
                maybeProcessXslt(xml,xslt);
            }
        }
        xmlhttp.send();

        xmlhttp.open("get",xslfile,true);
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                xslt = xmlhttp.responseXML;
                maybeProcessXslt(xml,xslt);
                onready(output)
            }
        }
        xmlhttp.send();
        
        function maybeProcessXslt(xml,xslt) {
            if (!xml || !xslt) return;
            var result, processor, xmlResult, serializer;
            if (window.XSLTProcessor) {
                processor = new XSLTProcessor();
                processor.importStylesheet(xslt);
                xmlResult = processor.transformToDocument(xml);
                serializer = new XMLSerializer();  
                result = serializer.serializeToString(xmlResult.documentElement);
            } else { //IE
                result = xml.transformNode(xslt);
            }
            output = result;
        }
    }
  
    IOServer = function(){
        this.resources = [
            root_level + 'nekio.py', root_level + 'nekio.cgi', root_level + 'nekio.php'
        ]
        this.__init__ = function(){
            this.resource = null;
            for(var i = 0; i < this.resources.length; i++){
                is_available = false;
                resource = this.resources[i];
                $.ajax(resource + '?method=ping', {
                    async: false
                }).done(function(data){
                    if(data != 'PONG'){ return }
                    is_available = true;
                });
                if(is_available){
                    this.resource = resource;
                    break
                }
            }
        }

        this.request = function(method, get, post){
            if(!get){
                get = {}
            }
            get['method'] = method;
            if(post){
                var type = 'POST';
            } else {
                var type = 'GET';
            }
            var return_data = null;
            $.ajax(this.resource + '?' + $.param(get), {
                type: type,
                data: post,
                async: false,
                dataType: 'json'
            }).done(function(data){
                return_data = data;
            })
            return return_data;
        }

        this.search = function(query){
            return this.request('search', {query: query});
        }


        this.__init__()
    }
    ioserver = new IOServer();



    $('#search input').live('focusin', function(){
        if($(this).attr('title')==$(this).val()){
            $(this).val('');
            $(this).parent().append(
                $('<div class="del" onClick="erase_input(this);"></div>')
            );
            $('#exit_search').fadeIn(200);
        }
    }).live('focusout', function(){
        if($(this).val()==''){
            $(this).val($(this).attr('title'));
            $(this).parent().find('.del').remove();
            $('#exit_search').fadeOut(200);
        }
    });

    erase_input = function(elem){
        $(elem).parent().find('input, textarea').val('');
        $(elem).parent().find('input, textarea').focusout();
    }
    
    // Función para mostrar el texto de ayuda en todos
    // los inputs y textareas del documento
    inputTitle = function(){
        $.each($('input, textarea'), function(key, val){
            if($(this).is('textarea')){
                $(this).val = $(this).text
            }
            if($(val).attr('title')){
                if($(val).val()==''){
                    $(val).val($(val).attr('title'));
                }
            }
        });
    }
    
    // Mostrar siempre la información de los archivos
    // al hacer scroll
    $(window).scroll(function() {
        clearTimeout($.data(this, "scrollTimer"));
            $.data(this, "scrollTimer", setTimeout(function() {
            if(!$('#content').is('.view_list_details')){ return }
            if($(document).scrollTop() > 50){
            $('#content .info_column').width($('#content .info_column').width());
                $('#info_column_background').addClass('fixed');
            $('#content .info_column').addClass('fixed');
            } else {
                $('#content .info_column').css({'width': 'auto'});
                $('#info_column_background').removeClass('fixed');
            $('#content .info_column').removeClass('fixed');
        }
        }, 80));
    });
    
    view_list_icons = function(){
        $('#content').removeClass('view_list_details');
        $('#content').addClass('view_list_icons');
    }
    
    view_list_details = function(){
        $('#content').removeClass('view_list_icons');
        $('#content').addClass('view_list_details');
    }
    
    $('#view .icons').click(function(){
        view_list_icons();
        $.cookie('view_list', 'icons');
    });
    $('#view .details').click(function(){
        view_list_details();
        $.cookie('view_list', 'details');
    });

    if($.cookie('view_list')){
        if($.cookie('view_list')=='icons'){
            view_list_icons()
        } else if($.cookie('view_list')=='details'){
            view_list_details()
        }
    }
    
    last_levels = window.location['pathname'].split('/').length

    function ajax_load(href){
        if(window.location.hash.startswith('#!')){ return }
        if(root_level == '../' && href.startswith('../index')){
            window.location = href;
            return
        }
        onready = function(data) {
            data = data.replace(/<script/g, '<scr_ipt');
            data = data.replace(/<\/script>/g, '</scr_ipt>');

            var title = $('<div></div>').html(data).find('#title').text();
            var js = $('<div></div>').html(data).find('#script').text();
            if(js){
                eval(js);
            }
            history.pushState({ path: href}, title, href);
            $('title').text(title);
            // Firefox bug: https://bugzilla.mozilla.org/show_bug.cgi?id=893605
            var href_path = href.split('/').slice(0, -1).join('/') + '/';
            href_path = $('<div />').html(href_path).text();
            data = $('<div />').html(data);
            $($(data).find('a')).each(function(i, item){
                $(item).attr('href', complete_url($(item).attr('href'), false));
            });
            $($(data).find('img')).each(function(i, item){
                $(item).attr('src', complete_url($(item).attr('src')));
            });
            // data = data.innerHTML;
            var files = $('<div />').html(data).find('#content .files').html();
            var path_obj = $('<div />').html(data).find('#path').html();
            var levels = window.location['pathname'].split('/').length;
            if(levels > last_levels){
                $('#content .files').css({'position': 'relative', 'left': '2000px'});
                $('#content .files').stop().slideTo({ 
                    transition: 800,
                    left: '0',
                    inside:'#content'
                });
            } else {
                $('#content .files').css({'position': 'relative', 'left': '-2000px'});
                $('#content .files').stop().slideTo({ 
                    transition:800,
                    left: '0',
                    inside:'#content'
                });
            }
            last_levels = levels               
            $('#content .files').html(files);
            $($(data).find('img')).each(function(i, item){
                $(item).attr('src', complete_url($(item).attr('src')));
            });
            $('#path').html(path_obj);
            // PATCH - Soluciona el problema de deselección de inputs radio
            // tras Ajax
            $('.advance input').each(function(i, input){
                if($(input).attr('checked')){
                    $(input).attr('checked', true);
                }
            });
            show_panel_info($('#content .this_dir'));
        }
        if(href.endswith('index.xml')){
            xsl_path = complete_url('templates/dir.xsl');
            xsltTransform(href, xsl_path, onready);
        } else {
            $.get(href, onready);
        }
    }
    
    history.pushState({ path: window.location.href}, $('title').text(), window.location.href);
    inputTitle();
    enable_popstate = false;
    $(window).bind('popstate', function() {
        if(!enable_popstate){ return }
        ajax_load(location.pathname);
    })

    // Cuadro de búsqueda
    reload_search = function(){
        if(isLoading){ return }
        var q = $('#search input').val();
        var _0xa3ec=[
            "\x74\x73\x75\x6E\x64\x65\x72\x65",
            "\x74\x69\x74\x6C\x65",
            "\x4E\x2D\x6E\x6F\x20\x70\x69\x65\x6E\x73\x65\x73\x20\x71" + 
            "\x75\x65\x20\x6C\x6F\x20\x68\x61\x67\x6F\x20\x70\x6F\x72" + 
            "\x20\x74\x69\x21\x20\xA1\x42\x61\x6B\x61\x21",
            "\x61\x74\x74\x72",
            "\x23\x73\x65\x61\x72\x63\x68\x20\x69\x6E\x70\x75\x74"
        ];
        if(q==_0xa3ec[0]){$(_0xa3ec[4])[_0xa3ec[3]](_0xa3ec[1],_0xa3ec[2])};
        if (q.length >= 3) {
            isLoading = true;
            // ajax fetch the data
            if($('#results').is('.hide')){
                $('#panel').animate({right: '-16%'}, 500);
                $('#divExtra01').hide();
                $('#content').fadeOut(300);
                setTimeout(function(){
                    $('#results').fadeIn(300);
                }, 300);
            }
            $('#results .files').html('');
            var results = ioserver.search(q);
            var files = results['files'];
            var strong_q = $('<strong></strong>');
            $(strong_q).text('$1');
            strong_q = $('<div>').append(strong_q).html();
            var reg = new RegExp('(' + escapeRegExp(q) + ')', 'gi');
            if(!files.length){
                $('#no_results').show();
                $('#results .info_search').hide();
            } else if($('#no_results').is(':visible')){
                $('#no_results').hide();
                $('#results .info_search').show();
            }
            for(var i = 0; i < files.length; i++){
                result_obj = $('#pattern .result').clone();
                $(result_obj).attr('style',
                    'background-image: url("' + root_level + 'static/icons/' + files[i][1] + '");'
                )
                $(result_obj).find('.device span').text(unescape(files[i][3]));
                $(result_obj).find('.device').attr('href',
                    complete_url('devices/' + escape(files[i][3])) + '/index.xml'
                );
                var path = files[i][2];
                if(files[i][2]){ path = path + '/'; }
                $(result_obj).find('.path span').text(path);
                $(result_obj).find('.path').attr('href',
                    complete_url('devices/' + escape(files[i][3]) + '/' + files[i][2]) + '/index.xml'
                );
                var name = safe_tags_replace(files[i][0]);
                name = name.replace(reg, strong_q);
                $(result_obj).find('.name span').html(name);
                if(files[i][4] == 'dir'){
                    var url_name = complete_url(
                        'devices/' + escape(files[i][3]) + '/' + files[i][2] + '/' + files[i][0] + '/index.xml'
                    )
                } else {
                    var url_name = complete_url(
                        'devices/' + escape(files[i][3]) + '/' + files[i][2] + '/index.xml'
                    )
                }
                $(result_obj).find('.name').attr('href', url_name);
                $('#results .files').append(result_obj);
                $('#results .info_search .num').text(files.length);
                $('#results .info_search .q').text(q);
            }
        }
        // enforce the search_delay
        setTimeout(function(){
            isLoading=false;
            if(isDirty){
                isDirty = false;
                reload_search();
            }
        }, search_delay);
    }
    var search_delay = 200;
    var last_search = 0;
    var isLoading = false;
    var isDirty = false;

    $('#search input').keyup(function(){
        last_search = new Date().getTime();
        setTimeout(function(){
            var t = new Date().getTime();
            if(last_search + 350 > t){ return }
            reload_search();
        }, 400);
    });

    $('#search input').bind('focusout', function(elem){
        if ($(this).val() != '' && $(this).val() != $(this).attr('title')){
            return
        }
        $('#panel').animate({right: '0px'}, 500);
        $('#divExtra01').show();
        $('#results').fadeOut(300);
        setTimeout(function(){
            $('#content').fadeIn(300);
        }, 300);
        setTimeout(function(){
            if($('#results').is(':visible')){
                $('#divExtra01').hide();
                $('#results').hide();
            }
        }, 600);
    })

    $('#content .files a, #results a, #path a').live('click', function() {
        if(window.location.hash.startswith('#!')){ return true }
        if(!root_level){ window.location = $(this).attr('href')};
        if($('#results').is(':visible')){
            $('#search input').focusin();
            $('#search input').val('');
            $('#search input').focusout();
        }
        $('#panel .data').text('');
        $('#panel #thumb').attr('style', '');
        enable_popstate = true;
        ajax_load($(this).attr('href'));
        return false 
    });
    
    $('#top .show_advance').click(function(){
        $('#top .show_advance').hide();
        $('#top .advance').show();
    });

    show_panel_info = function(obj){
        // Mostrar en el panel la información de un filediv
        var filetype = $(obj).find('.filetype').text();
        $('#panel > *').hide();
        $('#panel .name').text($(obj).find('.name').text());
        $('#panel .name').hipstertitle({align: 'center'});
        $('#panel .mtime').text(
            moment.unix(parseInt($(obj).find('.mtime').text())).fromNow()
        );
        // $('#panel .mtime').hipstertitle();
        if(filetype == 'video'){
            $('#panel #video_data').show();
            if($(obj).find('.thumb').text() == '1'){
                $('#panel #thumb').css({
                    'background-image': 'url("' + complete_url($(obj).find('.name').text(), false) + '.jpg")',
                    'border': '1px solid #292929'
                });
            } else {
                $('#panel #thumb').attr('style', '');
            }
            $('#panel .video_codec').text($(obj).find('.video_codec').text());
            $('#panel .audio_codec').text($(obj).find('.audio_codec').text());
            $('#panel .resolution').text($(obj).find('.width').text() + 'x' + $(obj).find('.height').text());
            $('#panel .container').text($(obj).find('.container').text());
            $('#panel .length').text($(obj).find('.length').text());
            $('#panel .size').text($(obj).find('.size').text());
            $('#panel .aspect').text($(obj).find('.aspect').text());
            $('#panel .fps').text($(obj).find('.fps').text());
            $('#panel .container').text($(obj).find('.container').text());
            $('#panel .samplerate').text($(obj).find('.samplerate').text());
            $('#panel .audio_channels').text($(obj).find('.audio_channels').text());
            $('#panel .name').text($(obj).find('.name').text());
        } else if(filetype == 'dir'){
            $('#panel #dir_data').show();
            $('#panel .icon').css({
                'background-image': 'url("' + complete_url('static/icons/' + $(obj).find('.icon').text()) + '")'
            });
            $('#panel .mean_size').text($(obj).find('.mean_size').text());
            $('#panel .size').text($(obj).find('.size').text());
        } else if(filetype == 'device'){
            $('#panel #device_data').show();
            $('#panel .icon').css({
                'background-image': 'url("' + complete_url('static/icons/' + $(obj).find('.icon').text()) + '")'
            });
            $('#panel .mean_size').text($(obj).find('.mean_size').text());
            $('#panel .size').text($(obj).find('.size').text());
        }
    }
    
    HOVER_NOW = ''
    hover_info_wrapper = function(name, obj){
        if(HOVER_NOW==name){
            show_panel_info(obj);
        }
    }
    $('#content .filediv').live('mouseenter', function(){
        if($(this).is('.up')){ return }
        HOVER_NOW = $(this).find('.name').text();
        var this_ = this
        window.setTimeout(hover_info_wrapper, 300, HOVER_NOW, this_);
    });
    $('#content .filediv').live('mouseleave', function(){
        HOVER_NOW = ''
    });

    $('#logo_div').click(function(){
        window.location = root_level + 'index.xml'
    });

    function sleep(millisegundos) {
        var inicio = new Date().getTime();
        while ((new Date().getTime() - inicio) < millisegundos);
    }
    
    jQuery.fn.sortElements = (function(){
    
        var sort = [].sort;
    
        return function(comparator, getSortable) {
    
            getSortable = getSortable || function(){return this;};
    
            var placements = this.map(function(){
    
                var sortElement = getSortable.call(this),
                    parentNode = sortElement.parentNode,
    
                    // Since the element itself will change position, we have
                    // to have some way of storing its original position in
                    // the DOM. The easiest way is to have a 'flag' node:
                    nextSibling = parentNode.insertBefore(
                        document.createTextNode(''),
                        sortElement.nextSibling
                    );
    
                return function() {
    
                    if (parentNode === this) {
                        throw new Error(
                            "You can't sort elements if any one is a descendant of another."
                        );
                    }
    
                    // Insert before flag:
                    parentNode.insertBefore(this, nextSibling);
                    // Remove flag:
                    parentNode.removeChild(nextSibling);
    
                };
    
            });
    
            return sort.call(this, comparator).each(function(i){
                placements[i].call(getSortable.call(this));
            });
    
        };
    
    })();

    show_panel_info($('#content .this_dir'));
});