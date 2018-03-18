$(document).ready( function(){
    var price, one_pay;

    [price, one_pay] = setAutoNumericMultipleMobileFriendly(['#id_full_price', '#id_initial_fee'], autoNumericCurrency)

    //sliders 
    $price_slider = $('.slider_price_home')
    $one_pay_slider = $('.slider_price_one')
    $years_slider = $('.slider_price_year')

    function setFormat(value, dec=0){
        return AutoNumeric.format(value, {
            digitGroupSeparator: ' ',
            decimalCharacter: ',',
            decimalPlaces: dec,
        });
    }

    function mortgage(mortgage_amount, years, mortgage_percentage) {
        months = years*12;
        monthly_mortgage_proportion = mortgage_percentage / 1200;
        monthly_payment = mortgage_amount * monthly_mortgage_proportion / (1 - Math.pow(1 + monthly_mortgage_proportion, -months))
        return Math.round(monthly_payment);
    }

    function calculator() {
        var percent;
        var years_number   = parseInt($('#id_years').val());
        

        if (years_number <= 5) {
            percent = 6.0;
        } else if (years_number <= 7) {
            percent = 7.4;
        } else if (years_number <= 12) {
            percent = 7.9
        } else {
            percent = 9.4;
        }

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
        right_border = (price.getNumber()*0.8)||$one_pay_slider.slider("option",'max')
        slider_val = $one_pay_slider.slider("value")
        one_pay_val = one_pay.getNumber();
        if (one_pay_val!=slider_val){
            slider_val = one_pay_val;
        }
        if (slider_val>right_border){
            slider_val = right_border;
        }

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
        years_number = parseInt($('#id_years').val()); 
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
        updateSliders();
        calculator();
    };

    $('.calc').mousemove(function(event) {
        recomputate();
    });

    $('input').change(function(){
        recomputate();
    })
    
    $years_slider.slider({
            animate: "slow",
            range: "min",
            value: $( "#id_years" ).val(),
            step: 1,
            min: 1,
            max: 30,
            slide: function( event, ui ) {
                $( "#id_years" ).val(  ui.value );
            }
        });

    $one_pay_slider.slider({
            animate: "slow",
            range: "min",
            value: one_pay.getNumber(),
            step: 10000,
            min: 0,
            max: 10000000,
            slide: function( event, ui ) {
                one_pay.set(ui.value);
            }
        });

    $price_slider.slider({
            animate: "slow",
            range: "min",
            value: price.getNumber(),
            step: 100000,
            min: 900000,
            max: 10000000,
            slide: function( event, ui ) {
                price.set(  ui.value );
            }
    });
    recomputate();
});
