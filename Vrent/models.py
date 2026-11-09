from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


# 1. VEHICLE CATEGORY

class VehicleCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def str(self):
        return self.name


# 2. VEHICLE

class Vehicle(models.Model):
    category = models.ForeignKey( VehicleCategory, on_delete=models.CASCADE,related_name='vehicles')
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    registration_number = models.CharField( max_length=50,unique=True  )
    model_year = models.IntegerField()
    seats = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    daily_rate = models.DecimalField( max_digits=10, decimal_places=2 )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='vehicles',  blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def str(self):
        return self.name


# 3. BOOKING

class Booking(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE,related_name='bookings')
    vehicle = models.ForeignKey(  Vehicle,on_delete=models.PROTECT,related_name='bookings'    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed'),
        ]
    status = models.CharField( max_length=20,choices=STATUS_CHOICES,default='pending')
    pickup_location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def str(self):
        return f"{self.user.username} - {self.vehicle.name}"


# 4. PAYMENT

class Payment(models.Model):
    booking = models.OneToOneField(Booking,on_delete=models.CASCADE,related_name='payment')
    amount = models.DecimalField( max_digits=10,decimal_places=2 )
    PAYMENT_METHOD_CHOICES = [
            ('cash', 'Cash'),
            ('upi', 'UPI'),
            ('card', 'Card'),
            ('bank', 'Bank Transfer'),
        ]
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES )
    PAYMENT_STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ]
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='pending')
    transaction_id = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def str(self):
        return f"Payment {self.id}"


# 5. REVIEW

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    vehicle = models.ForeignKey( Vehicle, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def str(self):
        return f"{self.vehicle.name} - {self.rating}/5"