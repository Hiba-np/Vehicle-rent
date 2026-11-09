from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *


# 1. USER REGISTRATION SERIALIZER

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =["id","username","password"]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




# 2. USER SERIALIZER

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields ="__all__"
    def get_full_name(self, obj):
        return obj.get_full_name()


# 3. VEHICLE CATEGORY SERIALIZER

class VehicleCategorySerializer(serializers.ModelSerializer):
    total_vehicles = serializers.SerializerMethodField()
    class Meta:
        model = VehicleCategory
        fields = "__all__"
    def get_total_vehicles(self, obj):
        return obj.vehicles.filter(is_available=True).count()


# 4. VEHICLE SERIALIZER

class VehicleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name',read_only=True)
    vehicle_age = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ['id', 'created_at']

    def get_vehicle_age(self, obj):
        from datetime import date
        return date.today().year - obj.model_year


# 5. BOOKING SERIALIZER

class BookingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    vehicle_name = serializers.SerializerMethodField()
    total_days = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = [ 'id','user','created_at']

    def get_username(self, obj):
        return obj.user.username

    def get_vehicle_name(self, obj):
        return obj.vehicle.name

    def get_total_days(self, obj):
        return (obj.end_date - obj.start_date).days

    def get_total_amount(self, obj):
        days = (obj.end_date - obj.start_date).days
        return days * obj.vehicle.daily_rate


    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        start = validated_data['start_date']
        end = validated_data['end_date']
        days = (end - start).days
        amount = days * vehicle.daily_rate
        booking = Booking.objects.create( **validated_data,total_days=days,total_amount=amount)
        return booking


# 6. PAYMENT SERIALIZER

class PaymentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    vehicle_name = serializers.SerializerMethodField()
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ['id','created_at']

    def get_username(self, obj):
        return obj.booking.user.username

    def get_vehicle_name(self, obj):
        return obj.booking.vehicle.name

    def create(self, validated_data):
        booking = validated_data['booking']
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            payment_method=validated_data['payment_method'])
        return payment


# 7. REVIEW SERIALIZER

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    vehicle_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = [ 'id','user','created_at']
    def get_username(self, obj):
        return obj.user.username

    def get_vehicle_name(self, obj):
        return obj.vehicle.name

