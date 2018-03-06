const autoNumericCurrency = {
    digitGroupSeparator: ' ',
    decimalCharacter: ',',
    minimumValue: 0,
    maximumValue: 100000000,
    currencySymbol: ' руб',
    currencySymbolPlacement: 's'
}

const autoNumericArea = {
    digitGroupSeparator: ' ',
    decimalCharacter: ',',
    minimumValue: 0,
    maximumValue: 1000,
    currencySymbol: ' м3',
    currencySymbolPlacement: 's'
}

$(document).ready(function() {
  var currencies = new AutoNumeric.multiple('.auto-numeric-currency', autoNumericCurrency);
  var areas = new AutoNumeric.multiple('.auto-numeric-area', autoNumericArea);

  autoNumericForm = $('.auto-numeric-currency, .auto-numeric-area').closest("form");
  autoNumericForm.submit(function(e){
    $(this).find('input.auto-numeric-currency, .auto-numeric-area').each(function(){
       var self=$(this);
       var v = AutoNumeric.getAutoNumericElement(this).getNumber();
       if (v){
         self.val(v);        
       }
   });
  })  

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

    $('.callback-link').magnificPopup({
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




