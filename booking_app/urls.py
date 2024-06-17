from django.contrib import admin
from django.urls import path
from booking_app.views import homepage
from booking_app.views import menupage
from booking_app.views import booking #,booking_success
from booking_app.views import tablebooking
from booking_app.views import signup, signin, signout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='home'),
    path('menu/',menupage,name='menu'),
    path('tablebooking/',tablebooking,name='tablebooking'),
    path('signup/',signup,name='signup'),
    path('signin/',signin,name='signin'),
    path('signup/',signout,name='signup'),
    path('booking/',booking,name='booking'),
    #path('booking_success/', booking_success, name='booking_success'),
]
