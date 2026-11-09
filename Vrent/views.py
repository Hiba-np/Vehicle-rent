from django.shortcuts import render
from Vrent.models import *
from Vrent.serializers import *
from Vrent.permissions import IsOwner,IsPaymentOwner
from rest_framework.permissions import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import *
from rest_framework.response import Response
from django.contrib.auth.models import User

# Create your views here.

# 1. USER REGISTRATION

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes=[TokenAuthentication]


# 2. USER LIST

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes=[TokenAuthentication]


# 3. VEHICLE CATEGORY

class VehicleCategoryListCreateView(ListCreateAPIView):
    queryset = VehicleCategory.objects.all()
    serializer_class = VehicleCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes=[TokenAuthentication]


class VehicleCategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleCategory.objects.all()
    serializer_class = VehicleCategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]


# 4. VEHICLE

class VehicleListCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes=[TokenAuthentication]


class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser]
    authentication_classes=[TokenAuthentication]


# 5. BOOKING

class BookingListCreateView(ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes=[TokenAuthentication]


# 6. PAYMENT

class PaymentListCreateView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(
            booking__user=self.request.user)


class PaymentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsPaymentOwner]
    authentication_classes=[TokenAuthentication]


# 7. REVIEW

class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes=[TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes=[TokenAuthentication]
 