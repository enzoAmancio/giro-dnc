import json
from django.shortcuts import redirect
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow
from .models import GoogleCalendarCredential
import os
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.conf import settings
from datetime import datetime, timedelta, timezone
from calendario.models import GoogleCalendarCredential, GoogleCalendarEvent

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Apenas para desenvolvimento local (HTTP)

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events"
]

def criar_evento_google(aula):
    # alunos da turma
    alunos = aula.turma.alunos.all()

    for aluno in alunos:
        cred = getattr(aluno.usuario, 'google_credentials', None)
        if not cred:
            continue  # pular quem não conectou o Google

        credentials = Credentials.from_authorized_user_info(cred.get_token())
        service = build("calendar", "v3", credentials=credentials)

        # Monta data/hora no formato ISO
        inicio = datetime.combine(aula.data, aula.hora_inicio).isoformat()
        fim = datetime.combine(aula.data, aula.hora_fim).isoformat()

        evento = {
            "summary": f"Aula: {aula.turma.nome}",
            "description": aula.tema or "Aula de dança",
            "start": {"dateTime": inicio, "timeZone": "America/Sao_Paulo"},
            "end": {"dateTime": fim, "timeZone": "America/Sao_Paulo"},
        }

        event_result = service.events().insert(calendarId="primary", body=evento).execute()

        GoogleCalendarEvent.objects.create(
            aula=aula,
            google_event_id=event_result['id']
        )

@login_required
def conectar_google(request):
    with open(settings.GOOGLE_CALENDAR_SECRET_PATH) as f:
        config_dict = json.load(f)

    flow = Flow.from_client_config(
        config_dict,
        scopes=SCOPES,
        redirect_uri=f"{settings.SITE_URL}/calendario/oauth2callback"
    )

    auth_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="true"
    )

    request.session["google_auth_flow"] = flow.client_config  # DADOS SERIALIZÁVEIS!

    return redirect(auth_url)

@login_required
def oauth2callback(request):
    with open(settings.GOOGLE_CALENDAR_SECRET_PATH) as f:
        config_dict = json.load(f)

    flow = Flow.from_client_config(
        config_dict,
        scopes=SCOPES,
        redirect_uri=f"{settings.SITE_URL}/calendario/oauth2callback"
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    GoogleCalendarCredential.objects.update_or_create(
        user=request.user,
        defaults={"token_json": credentials.to_json()}
    )

    return redirect("paginas:painel_index")
