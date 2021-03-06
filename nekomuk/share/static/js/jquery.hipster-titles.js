/*!
 * Hipster Titles
 *
 * Scrolling truncated text headers and whatever else.
 *
 * Version:  1
 * Released: 28-05-2013
 * Source:   https://github.com/Vheissu/jQuery-Hipster-Titles
 * Plugin:   hipstertitle
 * Author:   Dwayne Charrington (dwaynecharrington@gmail.com)
 * License:  MIT Licence
 *           http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright (c) 2013 Dwayne Charrington.
 *
 * Simple usage:
 *
 * var $headings = $(".thumbnail h4");
 *
 * if ($headings.length) {
 *     $headings.hipstertitle();
 * }
 *
 */
;(function ($, undefined) {

    $.fn.hipstertitle = function(options) {

        var settings = $.extend({
            'revealSpeed' : 2000,
            'revealEasing': 'linear',
            'hideSpeed': 800,
            'hideEasing': 'linear',
            'align': 'left',
        }, options);

        $(this).each(function() {

            var $this    = $(this);
            var $inner  = $this.children(":first");
            // For styling
            $this.addClass("hipster-title");

            // No child element, lets add one
            if ($inner.length <= 0) {
                $this.wrapInner("<span class='hipster-title-inner' />");
            } else {
                $inner.addClass('hipster-title-inner');
            }

            // Query for the inner child again
            $inner = $this.children('.hipster-title-inner');
            if(settings.align == 'center'){
                var $headingWidth = $this.width();
                var $innerWidth     = $inner.width();
                if($innerWidth <= $headingWidth){
                    $this.addClass('center');
                }
            }
            $this.mouseenter(function() {
                var $headingWidth = $this.width();
                var $innerWidth     = $inner.width();

                var subtract = $headingWidth - $innerWidth;

                // Inner is greater than the parent
                if ($innerWidth > $headingWidth) {
                    $inner.stop().animate({
                        left: subtract + 'px'
                    }, {
                        duration: settings.revealSpeed,
                        easing: settings.revealEasing
                    });
                }
            }).mouseleave(function() {
                $inner.stop().animate({
                    left: "0px"
                }, {
                    duration: settings.hideSpeed,
                    easing: settings.hideEasing
                });
            });

        });

    };

})( jQuery );
