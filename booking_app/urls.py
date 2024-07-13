"""
Standard and third party Imports
"""
from django.contrib import admin
from django.urls import path
from booking_app.views import homepage
from booking_app.views import menupage
from booking_app.views import login_view
from booking_app.views import signup_view, logout_view
from booking_app.views import table_booking_view, user_booking_list
from booking_app.views import user_booking_update, user_booking_delete


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),
    path('menu/', menupage, name='menu'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('booking/', table_booking_view, name='booking'),
    path('my-bookings/', user_booking_list, name='user_booking_list'),
    path('update_bookings/<int:booking_id>/',
         user_booking_update, name='user_booking_update'),
    path('delete_bookings/<int:booking_id>/',
         user_booking_delete, name='user_booking_delete'),
]
