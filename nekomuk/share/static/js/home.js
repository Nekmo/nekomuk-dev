$(document).ready(function(){
    last_hover_option = 0;
    end_hover_option = true;
    $('#box .option').hover(function(){
        option = this.classList[1];
        self = this;
        t = new Date().getTime();
        last_hover_option = t;
        setTimeout(function(){
            if(t + 150 < last_hover_option){ return }
            if(!end_hover_option){ return }
            if($("#more_info").find('.' + option).is(':visible')){
                return
            }
            end_hover_option = false;
            select_option_lock = true;
            $('#box .selected').removeClass('selected');
            $(self).addClass('selected');
            $('#more_info > *').fadeOut(250);
            setTimeout(function(){ 
                $('#more_info').find('.' + option).fadeIn(500, function(){
                    end_hover_option = true;
                });
            }, 300);
        }, 140);
    });

    $('#box .explore').click(function(){
        document.location = 'devices/index.xml';
    });

    $('#box .search').click(function(){
        setTimeout(function(){$('#search input').focus()}, 200);
        $('#start_search').fadeIn(300);
    });

    $('#search input').keyup(function(){
        $('#start_search').hide();
    });
});