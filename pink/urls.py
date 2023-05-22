from django.urls import path
from pink.views import data_partai_kompetisi_event

app_name = 'kependudukan'

urlpatterns = [
    # path('', show_kependudukan, name='show_kependudukan'),
    path('', data_partai_kompetisi_event, name='data_partai_kompetisi_event'),
    path('list-partai-kompetisi', data_partai_kompetisi_event, name='data_partai_kompetisi_event'),
    
]