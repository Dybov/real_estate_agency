$(document).ready( function(){
    var price_from;
    var price_to;
    var area_from;
    var area_to;
    var amount_of_rooms;
    var appropriate_buildings;

    var price_from_autonumeric;
    var price_to_autonumeric;
    var area_from_autonumeric;
    var area_to_autonumeric;

    [price_from_autonumeric, price_to_autonumeric] = new AutoNumeric.multiple('input[name="price"]', autoNumericCurrency);
    [area_from_autonumeric, area_to_autonumeric] = new AutoNumeric.multiple('input[name="area"]', autoNumericArea);

    function filterApartments() {
        // read filter params
        amount_of_rooms = $('input[name="rooms"]:checked').map(function(){
            if (this.value.includes('+')){
                // for rooms over than 4 or another big value
                num = [];
                val = parseInt(this.value, 10);
                for (var i = val; i < val+5; i++) {
                   num.push(String(i));
                }
                return num;
            }
            return this.value;
        }).get();

        appropriate_buildings = parseInt($('select.building-selects').val());
        price_from = price_from_autonumeric.getNumber();
        price_to = price_to_autonumeric.getNumber();
        area_from = area_from_autonumeric.getNumber();
        area_to = area_to_autonumeric.getNumber();

        appropriate_buildings_is_used = isNaN(appropriate_buildings)? false : true;
        amount_of_rooms_is_used = amount_of_rooms.length > 0 ? true: false;
        price_from_is_used = isNaN(price_from) ? false : price_from >= 0;
        price_to_is_used = isNaN(price_to) ? false : price_to > 0;
        area_from_is_used = isNaN(area_from) ? false : area_from >= 0;
        area_to_is_used = isNaN(area_to) ? false : area_to > 0; 

        $('.element-item').hide(); 

        var apartments = apartments_json.filter(function(apartment) {
            var out = appropriate_buildings_is_used ? apartment.fields.buildings.indexOf(appropriate_buildings)>-1 : true;
            out = out && (amount_of_rooms_is_used ? amount_of_rooms.indexOf(apartment.fields.rooms)>-1 : true);
            out = out && (price_from_is_used ? apartment.fields.price >= price_from: true);
            out = out && (price_to_is_used ? apartment.fields.price <= price_to: true);
            out = out && (area_from_is_used ? apartment.fields.total_area >= area_from: true);
            out = out && (area_to_is_used ? apartment.fields.total_area <= area_to: true);
            if (out){
                $('#apartment-'+apartment.pk).fadeIn('slow','easeOutBack');
                return out;
            }
        });
        if (apartments.length==0){
            $('#empty-filter-result').fadeIn('slow','easeOutBack');
        }
    }
    // filterApartments();
    $('input[name="rooms"]').add('input[name="area"]').add('input[name="price"]').add('.building-selects').change(function(){
        filterApartments();
    });
    filterApartments();
});