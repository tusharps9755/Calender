
import json
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import View
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'path/to/client_secret.json',  # Replace with your client_secret.json path
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        authorization_url, _ = flow.authorization_url(
            access_type='offline', prompt='consent'
        )
        return HttpResponseRedirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        flow = InstalledAppFlow.from_client_secrets_file(
            'path/to/client_secret.json',  # Replace with your client_secret.json path
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Save the credentials in the session or database for future use
        request.session['google_credentials'] = credentials.to_json()

        # Redirect to the view that lists the events
        return HttpResponseRedirect(reverse('event-list'))


class GoogleCalendarEventListView(View):
    def get(self, request):
        credentials_json = request.session.get('google_credentials')
        if not credentials_json:
            return HttpResponse('No Google credentials found.')

        credentials = Credentials.from_json(credentials_json)
        service = build('calendar', 'v3', credentials=credentials)

        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        return HttpResponse(json.dumps(events))
