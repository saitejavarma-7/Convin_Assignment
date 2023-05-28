from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from django.http import HttpResponse
import os
from googleapiclient.discovery import build

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# from django.shortcuts import render

import secrets
# Generate a random string for the state parameter
state = secrets.token_urlsafe(16)


def home_view(request):
    return render(request, 'base.html')

def event_view(request):
    return render(request,'events.html')

def GoogleCalendarInitView(request):
    flow = Flow.from_client_secrets_file(
        os.path.expanduser('./client_secret.json'),
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/'
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return redirect(authorization_url)

def GoogleCalendarRedirectView(request):
    state = request.session.get('state')  # Use get() method to retrieve state parameter
    if state is None:
        # Handle the case where the state parameter is missing
        return HttpResponse('State parameter is missing')
    else:
        flow = Flow.from_client_secrets_file(
            os.path.expanduser('./client_secret.json'),
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/',
            state=state)
        flow.fetch_token(authorization_response=request.get_full_path())
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return render(request, 'events.html', {'events': events})
