(function($) {
    $(document).ready(function() {
        // Only for stacked inlines
        $('div.inline-group div.inline-related:not(.tabular)').each(function() {
            fs = $(this).find('fieldset')
            h3 = $(this).find('h3:first')

            // Don't collapse if fieldset contains errors
            errors = h3.parent('div').find('.errorlist')
            // console.log(errors);
            if (errors.length>0){
                fs.addClass('stacked_collapse');
                h3.prepend('<a class="stacked_collapse-toggle" href="#">(' + gettext('Hide') + ')</a> ');
            }
            else {
                fs.addClass('stacked_collapse collapsed');
                h3.prepend('<a class="stacked_collapse-toggle" href="#">(' + gettext('Show') + ')</a> ');                
            }
            
            
            // Add toggle link
            h3.find('a.stacked_collapse-toggle').bind("click", function(){
                fs = $(this).parent('h3').parent('div').children('fieldset:first');
                if (!fs.hasClass('collapsed'))
                {
                    fs.addClass('collapsed');
                    $(this).html('(' + gettext('Show') + ')');
                }
                else
                {
                    fs.removeClass('collapsed');
                    $(this).html('(' + gettext('Hide') + ')');
                }
            }).removeAttr('href').css('cursor', 'pointer');
        });
    });
})(django.jQuery);