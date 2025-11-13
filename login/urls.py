from django.urls import path
from . import views

# Define o namespace 'login' para ser usado em {% url 'login:logout' %}
app_name = 'login'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
