from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from booking_app.views import homepage
from booking_app.views import menupage
#from booking_app.views import CustomLoginView
from booking_app.views import login_view
from booking_app.views import signup_view,logout_view,booking_table_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='home'),
    path('menu/',menupage,name='menu'),
    path('login/', login_view,name='login'),
    path('signup/',signup_view,name='signup'),
    path('logout/',logout_view,name='logout'),
    path('booking/',booking_table_view,name='booking'),
]
