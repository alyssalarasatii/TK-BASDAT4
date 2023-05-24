from django.urls import path
from pink.views import data_partai_kompetisi_event, data_hasil_pertandingan, c_latih_atlet,  r_atlet_dilatih, r_daftar_atlet

app_name = 'pink'

urlpatterns = [
    # path('', show_kependudukan, name='show_kependudukan'),
    path('', data_partai_kompetisi_event, name='data_partai_kompetisi_event'),
    path('list-partai-kompetisi', data_partai_kompetisi_event, name='data_partai_kompetisi_event'),
    path('hasil-pertandingan', data_hasil_pertandingan, name='data_hasil_pertandingan'),
    path('c-latih-atlet', c_latih_atlet, name='c_latih_atlet'),
    path('r-latih-atlet', r_atlet_dilatih, name='r_latih_atlet'),    
    path('/atlet/daftar-atlet', r_daftar_atlet, name='r_daftar_atlet'),    
    
]