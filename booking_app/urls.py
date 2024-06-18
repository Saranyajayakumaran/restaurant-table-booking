from django.contrib import admin
from django.urls import path
from booking_app.views import homepage
from booking_app.views import menupage
from booking_app.views import loginpage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='home'),
    path('menu/',menupage,name='menu'),
    path('login/',loginpage,name='login')
]
