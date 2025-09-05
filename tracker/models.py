from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_footprint = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

class FootprintEntry(models.Model):
    TRANSPORT_CHOICES = [('car','Car'), ('bus','Bus'), ('train','Train'), ('bike','Bike'), ('walk','Walk')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_km = models.FloatField()
    transport_mode = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    electricity_kwh = models.FloatField()
    renewable_energy = models.BooleanField(default=False)
    food_meat = models.FloatField()
    food_dairy = models.FloatField()
    food_plant = models.FloatField()
    waste_kg = models.FloatField()
    recycling_score = models.FloatField()
    water_liters = models.FloatField()
    shopping_spend = models.FloatField()
    prediction = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction:.2f}"
