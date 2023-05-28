from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView, home_view, event_view

urlpatterns = [
    path('', home_view, name='home'),
    path('events/',event_view, name = 'events'),
    path('rest/v1/calendar/init/', GoogleCalendarInitView, name='google_calendar_init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView, name='google_calendar_redirect'),
]
