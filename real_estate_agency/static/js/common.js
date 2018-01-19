$(function(){


function calclator(ipoteka) {

var price   = $('#id_full_price').val(),
    one_pay = $('#id_initial_fee').val(),
    //pay     = price * one_pay / 100,
    years   = $('#id_full_price').val();

if (years <= 7) {
var  percent = 7.4;
} else {
var  percent = 9.4;
  console.log( "меньше 7 лет" );
}


function ipoteka( price, onepay, years ) {
  var i = parseFloat( percent / 100 / 12 );
  var n = parseFloat( years * 12 );
  var r = ( price - one_pay ) * ( ( i * Math.pow( 1+i, n ) ) / ( Math.pow( 1+i, n ) - 1 ) );
  return r.toFixed(0);
  return r.toLocaleString();
}
var price_number = parseInt(price);
var all_price = price_number * percent / 100 * years + price_number;
var all_price_number = all_price.toLocaleString();

var price_mouth = ipoteka( price, one_pay, years )
var price_mouth_number = Number(price_mouth).toLocaleString();
console.log(price_mouth_number);



console.log("slozkenit " + (price_number + price_number));

console.log(" тест " + (price_number * percent / 100 * years + price_number));

$('.price_mouth').text(price_mouth_number);
$('.actual_prestnt').text(percent);
$('.all_price').text(all_price_number);

console.log( "Ежемесячный платеж: " + ipoteka( price, one_pay, years ) + " руб" );
console.log( "Ежемесячный платеж: " + years  + " лет" );
};

$('.calc').mousemove(function(event) {
 calclator();
});





  
});



$(document).ready(function() {

  $(".checkbox").click(function(e) {
    // Не надо preventDefault, т.к. там устанавливается значение checked
    // e.preventDefault();
$(this).parent(this).parent(this).toggleClass('active-checkbox')
  })





$('.search_form_select-select').styler();

    window.onload = function() { 
       $('.airSticky').airStickyBlock({
    debug: true, // Режим отладки, по умолчанию false
  stopBlock: '.airSticky_stop-block', // Класса контейнера, в котором находится сетка, по умолчанию .airSticky_stop-block
  offsetTop: 100 // отступ сверху
});
    };

  function classFunction(){
    if($('body').width()<769){ $('.airSticky').removeClass('airSticky')
    }
    else{

    }
  }
  
  classFunction();
  $(window).resize(classFunction);
   


$('.slider_price_year').slider({
        animate: "slow",
        range: "min",
        value: 7,
        step: 1,
        min: 1,
        max: 30,
        slide: function( event, ui ) {
            $( "#id_years" ).val(  ui.value );
            
        }
    });

$('.slider_price_one').slider({
        animate: "slow",
        range: "min",
        value: 35,
        step: 1,
        min: 1,
        max: 100,
        slide: function( event, ui ) {
          costValue = ui.value;
          costValue = costValue.toLocaleString();
            $( "#id_initial_fee" ).val(  costValue );
            
        }
    });

$('.slider_price_home').slider({
        animate: "slow",
        range: "min",
        value: 1200000,
        step: 100000,
        min: 900000,
        max: 10000000,
        slide: function( event, ui ) {
            $( "#id_full_price" ).val(  ui.value );
            
        }
    });





$(".toggle-mnu").click(function() {
  $(this).toggleClass("on");
  $(".menu_container").slideToggle();
  return false;
});

    // Custom JS
$('.slider_item').magnificPopup({
  type: 'image',
    fixedContentPos: false,
    fixedBgPos: true,
    overflowY: 'auto',
    closeBtnInside: true,
    preloader: false,
    midClick: true,
    mainClass: 'my-mfp-zoom-in',
    gallery:{
    enabled:true,
     }

});

    $('.documents_item').magnificPopup({
    type: 'inline',
    fixedContentPos: false,
    fixedBgPos: true,
    overflowY: 'auto',
    closeBtnInside: true,
    preloader: false,
    midClick: true,
    removalDelay: 300,
    mainClass: 'my-mfp-zoom-in',
    focus: '#popup_input'
    });

    $('.callback').magnificPopup({
    type: 'inline',
    fixedContentPos: false,
    fixedBgPos: true,
    overflowY: 'auto',
    closeBtnInside: true,
    preloader: false,
    midClick: true,
    removalDelay: 300,
    mainClass: 'my-mfp-zoom-in',
    focus: '#popup_input'
    });
    $('.pop_up_plan').magnificPopup({
    type: 'inline',
    fixedContentPos: false,
    fixedBgPos: true,
    overflowY: 'auto',
    closeBtnInside: true,
    preloader: false,
    midClick: true,
    removalDelay: 300,
    mainClass: 'my-mfp-zoom-in',
    focus: '#popup_input'
    });

    $('.slider_soc_prog_item').magnificPopup({
    type: 'inline',
    fixedContentPos: false,
    fixedBgPos: true,
    overflowY: 'auto',
    closeBtnInside: true,
    preloader: false,
    midClick: true,
    removalDelay: 300,
    mainClass: 'my-mfp-zoom-in',
    focus: '#popup_input'
    });

$('.popup_video').magnificPopup({
  type: 'iframe',
    fixedContentPos: false,
    fixedBgPos: true,
    overflowY: 'auto',
    closeBtnInside: true,
    preloader: false,
    midClick: true,
    mainClass: 'my-mfp-zoom-in'

});


});




