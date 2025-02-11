from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.db import transaction
from .models import CustomUser, Train, Booking
from .serializers import UserSerializer, TrainSerializer, BookingSerializer
from django.conf import settings

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.headers.get('X-API-KEY') == settings.ADMIN_API_KEY

class TrainCreateView(generics.CreateAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [AdminPermission]

@api_view(['GET'])
def seat_availability(request):
    source = request.query_params.get('source')
    destination = request.query_params.get('destination')
    trains = Train.objects.filter(source=source, destination=destination)
    serializer = TrainSerializer(trains, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def book_seat(request, train_id):
    try:
        with transaction.atomic():
            train = Train.objects.select_for_update().get(id=train_id)
            if train.available_seats > 0:
                train.available_seats -= 1
                train.save()
                Booking.objects.create(user=request.user, train=train)
                return Response({'status': 'Booking successful'}, status=status.HTTP_201_CREATED)
            return Response({'error': 'No seats available'}, status=status.HTTP_400_BAD_REQUEST)
    except Train.DoesNotExist:
        return Response({'error': 'Train not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def booking_details(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)