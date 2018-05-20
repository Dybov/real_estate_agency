function setFormat(value, dec=0){
    return AutoNumeric.format(value, {
        digitGroupSeparator: ' ',
        decimalCharacter: ',',
        decimalPlaces: dec,
    });
}

function endsWith(str, suffix){
    suffix=suffix+'';
    return str.indexOf(suffix, str.length-suffix.length) !== -1;
}

function yearsAppender(text){
    var suffix;
    text = text + '';
    if (endsWith(text, 1)){
        suffix = 'год';
    } else if (endsWith(text, 2) || endsWith(text, 3) || endsWith(text, 4)){
        suffix = 'года';
    } else {
        suffix = 'лет';
    }
    return text + ' ' + suffix;
}

function thousandCutter(value){
    var suffix;
    if (value > 1000){
        suffix = 'тыс.';
        value = parseInt(value/1000);
        if (value > 1000){
            suffix = 'млн.';
            value = parseInt(value/1000);
        }
    } 
    // value = setFormat(value);
    return value+' '+suffix;
}

$(document).ready( function(){
    var price, one_pay, recomputation_timer;
    var salary_card = $('#salary-card');
    var salary_proof_parent = $('#salary-proof').closest('.input-group');
    var builders_sales = $('#builders-sales');
    var builders_sales_parent = builders_sales.closest('.input-group');

    [price, one_pay] = setAutoNumericMultipleMobileFriendly(['#id_full_price', '#id_initial_fee'], autoNumericCurrency);
    years_element = $('#id_years');

    function setter(an_element, value){
        number = an_element.getNumber();
        if (!number){
            an_element.set(value);
        }
    };

    setter(price, 1200000);
    setter(one_pay, 1200000*0.15);
    if (!years_element.val()){
        years_element.val(15);
    }

    //sliders 
    $price_slider = $('.slider_price_home')
    $one_pay_slider = $('.slider_price_one')
    $years_slider = $('.slider_price_year')

    function setAppendixesForSlider(slider_el, appendix_class, callable_wrapper=null){
        var min_value = slider_el.slider('option', 'min');
        var max_value = slider_el.slider('option', 'max');
        var appendixes = $(appendix_class);
        var length = appendixes.length;
        if (length==0){
            return
        };
        var min_range = (max_value-min_value)/(length-1);
        
        var val;
        for (var i = 0; i < length; i++) {
            val = parseInt(min_range*i+min_value)
            if (typeof callable_wrapper === 'function'){
                val = callable_wrapper(val);
            };
            $(appendixes.get(i)).text(val);
        }
    }

    function mortgage(mortgage_amount, years, mortgage_percentage) {
        months = years*12;
        monthly_mortgage_proportion = mortgage_percentage / 1200;
        monthly_payment = mortgage_amount * monthly_mortgage_proportion / (1 - Math.pow(1 + monthly_mortgage_proportion, -months))
        return Math.round(monthly_payment);
    }

    function get_builders_sales(){
        var percent;
        var is_checked = $('#builders-sales').prop('checked');
        if (!is_checked){
            return 0;
        }

        var years_number = parseInt(years_element.val());
        if (years_number <= 7){
            percent = -2;
        } else if (years_number <= 12){
            percent = -1.5;
        } else {percent = 0;}

        return percent;
    }


    function other_pertcentage(){
        var perc_value = 0;
        var array_of_extra_fields = [
            '#salary-card',
            '#salary-proof',
            '#insurance',
            '#online-registration',
        ];

        array_of_extra_fields.forEach(function(element) {
            $input = $(element);
            field_val = parseFloat($input.val());
            if (element=='#salary-proof' && perc_value==-0.5){
                perc_by_field = field_val;
            } else {
                perc_by_field = $input.prop('checked')?field_val:0;                
            }
            perc_value = perc_value + perc_by_field;
        });
        perc_value = perc_value + get_builders_sales();
        return perc_value;
    }
    function update_checkboxes(){

        if (salary_card.prop('checked')){
            salary_proof_parent.slideUp();
        } else {
            salary_proof_parent.slideDown();
        }
        if (parseInt(years_element.val())>12){
            builders_sales.prop('checked', false);
        }
    }

    function calculator() {
        var percent = 11.5;
        var years_number   = parseInt(years_element.val());
        
        percent = percent + other_pertcentage();

        var price_number = price.getNumber();
        var one_pay_number = one_pay.getNumber();

        if (price_number < one_pay_number) {
            console.log('Нужно обработать');
            throw Exception('Первоначальный взнос не может быть равен или быть больше стоимости жилья');
        }
        var mortgage_amount = price_number - one_pay_number
        var price_per_month = mortgage( mortgage_amount, years_number, percent)
        $('.price_mouth').text(setFormat(price_per_month));
        $('.actual_prestnt').text(setFormat(percent, dec=1));
        $('.all_price').text(setFormat(mortgage_amount));
    };

    function updateOnePaySlider(){
        left_border = (price.getNumber()*0.15)||$one_pay_slider.slider("option",'min')
        right_border = (price.getNumber()*0.8)||$one_pay_slider.slider("option",'max')
        slider_val = $one_pay_slider.slider("value")
        one_pay_val = one_pay.getNumber();
        if (one_pay_val!=slider_val){
            slider_val = one_pay_val;
        };
        if (slider_val>right_border){
            slider_val = right_border;
        } else if (slider_val<left_border){
            slider_val = left_border;
        };

        $one_pay_slider.slider("option", "min", left_border);
        $one_pay_slider.slider("option", "max", right_border);
        $one_pay_slider.slider("value", slider_val);
        one_pay.set(slider_val);
    }

    function updatePriceSlider(){
        price_number = price.getNumber(); 
        if ($price_slider.slider("value")!=price_number){
            $price_slider.slider("value", price_number);
        }
    }

    function updateYearsSlider(){
        years_number = parseInt(years_element.val()); 
        if ($years_slider.slider("value")!=years_number){
            $years_slider.slider("value", years_number);
        }
    }

    function updateSliders(){
        updateOnePaySlider();
        updatePriceSlider();
        updateYearsSlider();
    }

    function recomputate(){
        update_checkboxes();
        clearTimeout(recomputation_timer);
        recomputation_timer = setTimeout(function(){
            updateSliders();
            setAppendixesForSlider($one_pay_slider, '.slider-initial-appendix', thousandCutter);
            calculator();
            }, 
            400
        );
    };

    $('input').change(function(){
        recomputate();
    })
    
    $years_slider.slider({
            // animate: "fast",
            range: "min",
            value: $( "#id_years" ).val(),
            step: 1,
            min: 1,
            max: 30,
            slide: function( event, ui ) {
                $( "#id_years" ).val(  ui.value );
                recomputate();
            }
        });

    $one_pay_slider.slider({
            // animate: "fast",
            range: "min",
            value: one_pay.getNumber(),
            step: 10000,
            min: 0,
            max: 10000000,
            slide: function( event, ui ) {
                one_pay.set(ui.value);
                recomputate();
            }
        });

    $price_slider.slider({
            //animate: "fast",
            range: "min",
            value: price.getNumber(),
            step: 100000,
            min: 900000,
            max: 10000000,
            slide: function( event, ui ) {
                price.set(  ui.value );
                recomputate();
            }
    });
    recomputate();
    setAppendixesForSlider($price_slider, '.slider-price-appendix', thousandCutter);
    setAppendixesForSlider($years_slider, '.slider-years-appendix', yearsAppender);
    $("#mortgage-calc-callback").click(function(e){
        price
        $("#modal_callback input[type='hidden'][name!='csrfmiddlewaretoken']").val(
            ' \nИнтересует ипотечный калькулятор с параметрами:\nСтоимость: '+
                price.getFormatted()
            + '\nВзнос: ' +
                one_pay.getFormatted()
            + '\nЛет: ' +
            parseInt(years_element.val()) + '\n' +
            "Платеж: " + $('.price_mouth').text() + 'руб.'
        );
    })
});