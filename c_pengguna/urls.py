from django.urls import path
from c_pengguna.views import register
from c_pengguna.views import register_atlet
from c_pengguna.views import register_pelatih
from c_pengguna.views import register_umpire
app_name = 'c_pengguna'
urlpatterns = [
    path('', register, name='register'),
    path('umpire/', register_umpire, name='register-umpire'),
    path('atlet/', register_atlet, name='register-atlet'),
    path('pelatih/', register_pelatih, name='register-coach'),
]
