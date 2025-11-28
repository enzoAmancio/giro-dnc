app_name = 'calendario'
from django.urls import path
from .views import conectar_google, oauth2callback

urlpatterns = [
    path('conectar-google/', conectar_google, name="conectar_google"),
    path('oauth2callback', oauth2callback, name="oauth2callback"),
]
