from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView, GoogleCalendarEventListView

urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='redirect'),
    path('rest/v1/calendar/events/', GoogleCalendarEventListView.as_view(), name='event-list'),
]