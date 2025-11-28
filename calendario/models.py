from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.

class GoogleCalendarCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='google_credentials')
    token_json = models.TextField()  # Salvamos o token em JSON aqui
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Credenciais do Google de {self.user.username}"

    # Para facilitar: transforma o texto em JSON ao usar
    def get_token(self):
        return json.loads(self.token_json)

    def set_token(self, token_dict):
        self.token_json = json.dumps(token_dict)
        self.save()
        
class GoogleCalendarEvent(models.Model):
    aula = models.OneToOneField('paginas.Aula', on_delete=models.CASCADE, related_name='google_evento')
    google_event_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evento Google da aula {self.aula}"