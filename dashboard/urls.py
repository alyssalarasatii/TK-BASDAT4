from django.urls import path
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    # # path('', data_partai_kompetisi_event, name='data_partai_kompetisi_event'),
    path('dashboard-atlet', dashboard_atlet, name='dashboard_atlet'),
    path('dashboard-pelatih', dashboard_p, name='dashboard_p'),
    path('dashboard-umpire', dashboard_u, name='dashboard_u'),

]