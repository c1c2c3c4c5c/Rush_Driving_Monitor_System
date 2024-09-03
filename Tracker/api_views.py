from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json

from Tracker.models import *


class TrackerEndpointSet:
    @staticmethod
    @csrf_exempt
    def post_current_location(request, nid):
        try:
            node = TrackerNode.objects.get(node_id=nid)
            data = request.GET
            location = LocationHistory.objects.create(
                trip=Trip.objects.filter(node=node, is_active=True).first(),
                latitude=data.get("lat"),
                longitude=data.get("lon"),
                city=data.get("city"),
                region=data.get("region"),
                country=data.get("country"),
            )
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed"})

    @staticmethod
    def post_trip_event(request, nid):
        try:
            etype = request.GET.get("etype")
            node = TrackerNode.objects.get(node_id=nid)
            trip = Trip.objects.filter(node=node, is_active=True).first()
            if etype == "fast_lane_change":
                etype = "HARSH_LANE_CHANGE"
            elif etype == "hard_braking":
                etype = "HARD_BRAKING"
            elif etype == "rapid_acceleration":
                etype = "RAPID_ACCELERATION"
            TripEvent.objects.create(trip=trip, event_type=etype)
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed"})

    @staticmethod
    @require_GET
    @login_required
    def get_current_location(request, nid):
        trip = Trip.objects.filter(node__node_id=nid, is_active=True).first()
        lh = LocationHistory.objects.filter(trip=trip).last()
        return JsonResponse({
            "lat": lh.latitude if lh else None,
            "lon": lh.longitude if lh else None,
            "city": lh.city if lh else None,
            "region": lh.region if lh else None,
            "country": lh.country if lh else None,
        })
