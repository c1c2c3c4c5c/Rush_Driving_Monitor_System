import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Tracker.models import *


# Create your views here.


@login_required(login_url='/login/')
def dashboard(request):
    context = {
        'pagename': 'dashboard',
    }
    return render(request, "pages/logistics/home.html", context)


@login_required(login_url='/login/')
def fleet_demo(request):
    data = {
        'pagename': 'fleet-demo',
        "vehicles": [
            {
                "id": 1,
                "number": "One",
                "name": "GJ 12 KW 1234",
                "location": "Ahmedabad, Gujarat",
                "progress": 67,
                "latitude": 23.0225,
                "longitude": 72.5714,
                "events": [
                    {
                        "driver": "Harjeet Singh",
                        "time": "Sep 03, 8:02 AM",
                        "type": "danger",
                        "behavior": "Harsh Braking"
                    },
                    {
                        "driver": "Harjeet Singh",
                        "time": "Sep 03, 10:34 AM",
                        "type": "warning",
                        "behavior": "Aggressive Acceleration"
                    },
                    {
                        "driver": "Harjeet Singh",
                        "time": "Sep 03, 3:54 PM",
                        "type": "warning",
                        "behavior": "Harsh Lane Change"
                    },
                    {
                        "driver": "Harjeet Singh",
                        "time": "Sep 03, 5:12 PM",
                        "type": "danger",
                        "behavior": "Harsh Braking"
                    }
                ]
            },
            {
                "id": 2,
                "number": "Two",
                "name": "MH 05 AB 5678",
                "location": "Mumbai, Maharashtra",
                "progress": 45,
                "latitude": 19.0760,
                "longitude": 72.8777,
                "events": [
                    {
                        "driver": "Rahul Sharma",
                        "time": "Sep 04, 9:15 AM",
                        "type": "warning",
                        "behavior": "Aggressive Lane Change"
                    },
                    {
                        "driver": "Rahul Sharma",
                        "time": "Sep 04, 11:47 AM",
                        "type": "danger",
                        "behavior": "Harsh Braking"
                    },
                    {
                        "driver": "Rahul Sharma",
                        "time": "Sep 04, 2:30 PM",
                        "type": "warning",
                        "behavior": "Aggressive Acceleration"
                    },
                    {
                        "driver": "Rahul Sharma",
                        "time": "Sep 04, 4:18 PM",
                        "type": "danger",
                        "behavior": "Harsh Braking"
                    }
                ]
            },
            {
                "id": 3,
                "number": "Three",
                "name": "DL 03 XY 9876",
                "location": "Delhi, NCR",
                "progress": 80,
                "latitude": 28.6139,
                "longitude": 77.2090,
                "events": [
                    {
                        "driver": "Suman Gupta",
                        "time": "Sep 05, 7:30 AM",
                        "type": "danger",
                        "behavior": "Harsh Braking"
                    },
                    {
                        "driver": "Suman Gupta",
                        "time": "Sep 05, 10:15 AM",
                        "type": "warning",
                        "behavior": "Aggressive Acceleration"
                    }
                ]
            },
            {
                "id": 4,
                "number": "Four",
                "name": "TN 09 CD 4321",
                "location": "Chennai, Tamil Nadu",
                "progress": 60,
                "latitude": 13.0827,
                "longitude": 80.2707,
                "events": [
                    {
                        "driver": "Priya Verma",
                        "time": "Sep 06, 9:45 AM",
                        "type": "danger",
                        "behavior": "Harsh Lane Change"
                    },
                    {
                        "driver": "Priya Verma",
                        "time": "Sep 06, 2:20 PM",
                        "type": "warning",
                        "behavior": "Aggressive Acceleration"
                    }
                ]
            },
            {
                "id": 5,
                "number": "Five",
                "name": "KA 08 PQ 7890",
                "location": "Bangalore, Karnataka",
                "progress": 55,
                "latitude": 12.9716,
                "longitude": 77.5946,
                "events": [
                    {
                        "driver": "Amit Patel",
                        "time": "Sep 07, 11:10 AM",
                        "type": "danger",
                        "behavior": "Harsh Braking"
                    },
                    {
                        "driver": "Amit Patel",
                        "time": "Sep 07, 3:55 PM",
                        "type": "warning",
                        "behavior": "Aggressive Lane Change"
                    }
                ],
            }

        ]
    }
    data['vehicles_json'] = json.dumps(data['vehicles'])
    return render(request, "pages/logistics/fleet.html", data)


@login_required(login_url='/login/')
def fleet(request):
    nodes = TrackerNode.objects.filter(group=Organization.objects.get(user=request.user))
    trips = Trip.objects.filter(node__in=nodes, is_active=True)
    print(trips)
    vehicle_data = []
    for i, t in enumerate(trips):
        print(t.id)
        lh = LocationHistory.objects.filter(trip=t).last()
        events = []
        for event in TripEvent.objects.filter(trip=t).order_by('-event_time'):
            events.append({
                "driver": t.driver.name,
                "time": event.event_time.strftime("%b %d, %I:%M %p"),
                "type": "danger" if event.event_type == "HARD_BRAKING" else "warning",
                "behavior": dict(event.EVENT_TYPES)[event.event_type]
            })

        vehicle_data.append({
            "id": i + 1,
            "number": f"N{t.node.vehicle.number}",
            "name": t.node.vehicle.number,
            "node_id": t.node.node_id,
            "location": t.node.vehicle.name,
            "progress": t.node.vehicle.id*10,
            "latitude": float(lh.latitude) if lh else None,
            "longitude": float(lh.longitude) if lh else None,
            "events": events
        })
    data = {
        'pagename': 'fleet',
        "vehicles": vehicle_data
    }
    data['vehicles_json'] = json.dumps(data['vehicles'])
    return render(request, "pages/logistics/fleet-live.html", data)


@login_required(login_url='/login/')
def trip(request):
    if request.method == "POST":
        if request.POST.get('method') == "create":
            node = TrackerNode.objects.get(pk=request.POST.get('node'))
            driver = Driver.objects.get(pk=request.POST.get('driver'))
            t = Trip.objects.create(node=node, driver=driver)
            t.is_active = True
            t.save()
        if request.POST.get('method') == "delete":
            trip = Trip.objects.get(pk=request.POST.get('trip_id'))
            trip.end_time = datetime.now()
            trip.is_active = False
            trip.save()
    nodes = TrackerNode.objects.filter(group=Organization.objects.get(user=request.user))
    trips = Trip.objects.filter(node__in=nodes)
    print(trips)
    context = {
        'pagename': 'trips',
        "nodes": nodes,
        "drivers": Driver.objects.filter(group=Organization.objects.get(user=request.user)),
        "trips": trips
    }
    return render(request, "pages/logistics/trips.html", context)


@login_required(login_url='/login/')
def hawk_node(request):
    nodes = TrackerNode.objects.filter(group=Organization.objects.get(user=request.user))
    print(nodes)
    context = {
        'pagename': 'hawk_node',
        "nodes": nodes
    }
    return render(request, "pages/logistics/nodes.html", context)


@login_required(login_url='/login/')
def analysis(request):
    context = {
        'pagename': 'analysis',
        "nodes": [
            {
                "id": 1,
                "name": "GJ 12 KW 1234",
                "location": "Ahmedabad, Gujarat",
                "latitude": 23.0225,
                "longitude": 72.5714,
                "organization": "ABC Logistics",
                "is_active": True,
                "last_updated": "Sep 03, 8:02 AM",
            },
            {
                "id": 2,
                "name": "MH 05 AB 5678",
                "location": "Mumbai, Maharashtra",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "organization": "ABC Logistics",
                "is_active": True,
                "last_updated": "Sep 04, 9:15 AM",
            },
            {
                "id": 3,
                "name": "DL 03 XY 9876",
                "location": "Delhi, NCR",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "organization": "ABC Logistics",
                "is_active": False,
                "last_updated": "Sep 05, 7:30 AM",
            },
            {
                "id": 4,
                "name": "TN 09 CD 4321",
                "location": "Chennai, Tamil Nadu",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "organization": "ABC Logistics",
                "is_active": True,
                "last_updated": "Sep 06, 9:45 AM",
            },
            {
                "id": 5,
                "name": "KA 08 PQ 7890",
                "location": "Bangalore, Karnataka",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "organization": "ABC Logistics",
                "is_active": False,
                "last_updated": "Sep 07, 11:10 AM",
            }

        ]
    }
    return render(request, "pages/logistics/analysis.html", context)
