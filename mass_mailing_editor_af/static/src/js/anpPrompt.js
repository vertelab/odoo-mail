/*
* jQuery anpIprompt
* By: Johan Nilsson
*/
;(function ($) {
    $.anpPrompt = function () {
        var ignore, noTop = true;

        if (arguments.length > 1) {
            if (arguments[1].hasOwnProperty('ignoreB')) {
                ignore = arguments[1].ignoreB;
            }
            //Apply default style if none exists
            if (!arguments[1].hasOwnProperty('show')) {
                arguments[1].show = 'fadeIn';
            }
            if (arguments[1].hasOwnProperty('top')) {
                noTop = false;
            }
        } else {
            //Fetch html style and then create a new array to apply the style
            var defaultStyle = arguments[0],
                apsisStyle = { show: 'fadeIn' };

            arguments = [];
            //Fix for empty messages. Should never happend. But we rather have a fix for it.
            //The error apears in the $.prompt so this is a fix for $.prompt
            if (typeof (defaultStyle) === "undefined") {
                defaultStyle = ' ';
            }
            arguments[0] = defaultStyle;
            arguments[1] = apsisStyle;
        }

        return $.prompt.apply(this, arguments)
        .find('.jqibuttons button').each(function () {
            var me = $(this),
                text = me.text();
            me.html('<span><em>' + text + '</em></span>');
            //If ignore is null, then do nothing
            if (ignore != null || typeof (ignore) != "undefined") {

                for (var i = 0; i < ignore.length; i++) {
                    if (me.val() == ignore[i]) {
                        me.attr('disabled', 'disabled').find('em').addClass('anp-button-disabled');
                    }
                }
            }

            if(noTop) {
                var content = me.closest('div#jqi'),
                    topVal = (($(window).height() - content.outerHeight()) / 2) + $(window).scrollTop() + "px";
                content.css('top', topVal);

                //Add resize event when the window is chainging size.
                $(window).resize(function(){
                    var content = $('div#jqi'),
                        topVal = (($(window).height() - content.outerHeight()) / 2) + $(window).scrollTop() + "px";
                    content.css('top', topVal);
                });
            }
        }).end() //End .jqibuttons FIND
        .find('.jqi').each(function() {
            
            //Bind esc to be a close
            $(window).ready(function(){
                $(document).keyup(function(e) {
                    if (e.keyCode == 27) {/* esc */
                        $.prompt.close();
                    }
                });
            });
            
            var me = $(this),
                buttons = me.find('.jqibuttons'),
                buttonWidth = 0;
            /* If needed we change the modals width if the buttons is wider than the modals size */

            //For IE
            buttons.find('button').each(function() { buttonWidth += $(this).width(); });
            if(buttonWidth > 480) { me.find('.jqicontainer').css({'max-width': (buttonWidth+20)+"px"}); }

            if($.browser.msie && $.browser.version <= 8) {
                var parent = $(this).closest('.jqibox'),
                    theBox = $('.jqi'),
                    close = $('div.jqiclose'),
                    isHistory = $('div#SubscriberHistory').length;
                
                if(typeof(theBox) !== "undefined") {
                    parent.append(close);
                    close.css({
                        top: (theBox.position().top - 16) + "px",
                        left: (theBox.position().left + ((theBox.width()/2)-7)) + "px"
                    });

                    if(isHistory) {
                        setTimeout(function(){
                            close.css({
                                top: (theBox.position().top - 16) + "px",
                                left: (theBox.position().left + ((theBox.width()/2))) + "px"
                            });
                        }, 5);
                    }
                }

                //Close button does not get removed directly since I had to move it to the dimarea
                close.click(function(){$(this).remove();});

                $(window).resize(function(){
                    var parent = $('.jqibox'),
                    theBox = $('.jqi'),
                    close = $('div.jqiclose');
                    if(theBox.width() !== null || theBox.position() !== null){
                        if(isHistory && typeof(theBox) !== "undefined") {
                            setTimeout(function(){
                                close.css({
                                    top: (theBox.position().top - 16) + "px",
                                    left: (theBox.position().left + ((theBox.width()/2)-7)) + "px"
                                });
                            }, 5);
                        }else {
                            if(typeof(theBox) !== "undefined") {
                                close.css({
                                    top: (theBox.position().top - 16) + "px",
                                    left: (theBox.position().left + ((theBox.width()/2)-7)) + "px"
                                });
                            }
                        }
                    }
                });
            }
        }) //End .jqi FIND
        .end()
        ;
    };
})(jQuery);