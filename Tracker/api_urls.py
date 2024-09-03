from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from DrivingMonitor import settings
from Tracker.api_views import *

urlpatterns = [
    path('node/<str:nid>/latest_location/', TrackerEndpointSet.get_current_location),
    path('node/<str:nid>/latest_location', TrackerEndpointSet.get_current_location),
    path('node/<str:nid>/latest_location/create/', TrackerEndpointSet.post_current_location),
    path('node/<str:nid>/latest_location/create', TrackerEndpointSet.post_current_location),
    path('node/<str:nid>/event/create/', TrackerEndpointSet.post_trip_event),
    path('node/<str:nid>/event/create', TrackerEndpointSet.post_trip_event),
]
