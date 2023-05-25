from django.urls import path
from ungu.views import event_cards
from ungu.views import sponsor_form, event_cards_partai

app_name = 'ungu'

urlpatterns = [
    path('', event_cards, name='event_cards'),
    path('events', event_cards, name='event_cards'),
    path('daftar_sponsor', sponsor_form, name='sponsor_form'),
    path('events-partai', event_cards_partai, name='event_cards_partai'),

]