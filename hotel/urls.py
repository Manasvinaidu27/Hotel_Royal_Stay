from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.make_booking, name='make_booking'),
    path('rooms/<int:room_id>/review/', views.add_review, name='add_review'),
    path('recommendations/', views.room_recommendations, name='room_recommendations'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
