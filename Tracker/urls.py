from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from DrivingMonitor import settings
from Tracker.views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('api/', include('Tracker.api_urls')),
    path('fleet/', fleet, name='fleet'),
    path('fleet-demo/', fleet_demo, name='fleet-demo'),
    path('trips/', trip, name='trips'),
    path('nodes/', hawk_node, name='nodes'),
    path('analysis/', analysis, name='analysis'),
]
