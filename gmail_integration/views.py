import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configura el flujo OAuth2
flow = Flow.from_client_secrets_file(
    'citas/config/credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.labels']
)
flow.redirect_uri = 'http://localhost:8000/gmail/oauth2callback2/'

def gmail_auth(request):
    if 'credentials' in request.session:
        del request.session['credentials']
    authorization_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return redirect(authorization_url)

def oauth2callback2(request):
    try:
        flow.fetch_token(code=request.GET.get('code'))
        credentials = flow.credentials
        
        # Guarda las credenciales en la sesión
        request.session['credentials'] = credentials_to_dict(credentials)
        logger.info("Credenciales guardadas exitosamente")
        
        return redirect('gmail_inbox')
    except Exception as e:
        logger.error(f"Error en oauth2callback: {e}")
        return HttpResponse("Error during authentication process", status=400)

def gmail_inbox(request):
    if 'credentials' not in request.session:
        logger.info("No se encontraron credenciales, redirigiendo a autenticación")
        return redirect('gmail_auth')
    
    try:
        credentials = Credentials(**request.session['credentials'])
        
        # Verifica si el token ha expirado y refresca si es necesario
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            request.session['credentials'] = credentials_to_dict(credentials)

        service = build('gmail', 'v1', credentials=credentials)
        
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        email_list = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_list.append({
                'id': msg['id'],
                'subject': next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), 'No Subject'),
                'snippet': msg['snippet']
            })
        
        return render(request, 'gmail_inbox.html', {'email_list': email_list})
    except HttpError as error:
        logger.error(f"Error al acceder a Gmail: {error}")
        if error.resp.status == 401:
            # Token expirado o inválido, intentar refrescar
            del request.session['credentials']
            return redirect('gmail_auth')
        elif error.resp.status == 403:
            return HttpResponse("Permisos insuficientes para acceder a los correos", status=403)
    return HttpResponse("Error al acceder a tus correos de Gmail", status=500)


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }