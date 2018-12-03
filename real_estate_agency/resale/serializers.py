from rest_framework import serializers

from .models import ResaleApartment, ResaleApartmentImage


class ResaleApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResaleApartmentImage
        fields = '__all__'


class ResaleApartmentSerializer(serializers.ModelSerializer):
    # images = ResaleApartmentImageSerializer(source='photos', many=True)
    get_building_type_display = serializers.ReadOnlyField()
    price_per_square_meter = serializers.ReadOnlyField()
    neighbourhood = serializers.StringRelatedField()
    decoration = serializers.ReadOnlyField(source='decoration.name')

    class Meta:
        model = ResaleApartment
        fields = (
            'total_area',
            'address',
            'floor',
            'number_of_storeys',
            # 'images',
            'full_price',
            'old_price',
            'price_per_square_meter',
            'neighbourhood',
            'get_building_type_display',
            'number_of_storeys',
            'date_of_construction',
            'celling_height',
            'decoration',
            'kitchen_area',
            'balcony_area',
            'id',
        )
