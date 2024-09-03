from django.db import models


# Create your models here.


class Organization(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1024)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.active}"

    def save(self, *args, **kwargs):
        if self.id is None:
            # self.user.set_password('12345678')
            self.user.user_permissions.remove(*self.user.user_permissions.all())
            self.user.is_staff = True
            self.user.is_superuser = False
            self.user.is_active = True
            self.user.save()
        super(Organization, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Organizations"
        verbose_name = "Organization"


class Vehicle(models.Model):
    group = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    number = models.CharField(max_length=1024)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.number} | {self.group.name}"

    class Meta:
        verbose_name_plural = "Vehicles"
        verbose_name = "Vehicle"


class Driver(models.Model):
    group = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    phone = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    license_number = models.CharField(max_length=1024)
    license_expiry = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=1024)
    country = models.CharField(max_length=1024)
    pincode = models.CharField(max_length=1024)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.group.name}"

    class Meta:
        verbose_name_plural = "Drivers"
        verbose_name = "Driver"


def generate_random_string(length=10):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters.upper()) for i in range(length))


class TrackerNode(models.Model):
    node_id = models.CharField(max_length=10, unique=True, default=generate_random_string)
    is_online = models.BooleanField(default=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Tracker Node {self.node_id} | Online Status: {self.is_online}"

    class Meta:
        verbose_name_plural = "Tracker Nodes"
        verbose_name = "Tracker Node"


class Trip(models.Model):
    node = models.ForeignKey(TrackerNode, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.node} | Start {self.start_time} | End: {self.end_time}"

    class Meta:
        verbose_name_plural = "Trips"
        verbose_name = "Trip"


class TripEvent(models.Model):
    EVENT_TYPES = (
        ("HARD_BRAKING", "Hard Braking"),
        ("RAPID_ACCELERATION", "Rapid Acceleration"),
        ("HARSH_LANE_CHANGE", "Harsh Lane Change"),
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=1024, choices=EVENT_TYPES)
    event_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trip} | {self.event_type} | {self.event_time}"

    class Meta:
        verbose_name_plural = "Trip Events"
        verbose_name = "Trip Event"


class LocationHistory(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, default=None, null=True, blank=True)
    latitude = models.DecimalField(max_digits=50, decimal_places=6)
    longitude = models.DecimalField(max_digits=50, decimal_places=6)
    city = models.CharField(max_length=1024, default='NA')
    region = models.CharField(max_length=1024, default='NA')
    country = models.CharField(max_length=1024, default='NA')

    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.latitude)}, {str(self.longitude)} | {self.timestamp}"

    class Meta:
        verbose_name_plural = "Location History Timeline"
        verbose_name = "Location History"
