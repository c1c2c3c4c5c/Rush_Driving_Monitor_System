from django.contrib import admin
from Tracker.models import *
# Register your models here.


admin.site.register(Organization)
admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(TrackerNode)
admin.site.register(Trip)
admin.site.register(TripEvent)
admin.site.register(LocationHistory)
