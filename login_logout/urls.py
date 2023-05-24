from django.urls import path
from login_logout.views import login, logout

app_name = 'login-logout'

urlpatterns = [
    # path('', data_partai_kompetisi_event, name='data_partai_kompetisi_event'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
]