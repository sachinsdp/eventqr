from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=200)
    reg_no = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MealScan(models.Model):
    participant = models.ForeignKey("Participant", on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    meal = models.CharField(max_length=20)
    scanned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("participant", "day", "meal")

    def __str__(self):
        return f"{self.participant.name} - Day {self.day} - {self.meal}"
