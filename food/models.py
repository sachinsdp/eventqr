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




class Panel(models.Model):

    name = models.CharField(max_length=200)
    day = models.IntegerField()

    def __str__(self):
        return self.name


class Panelist(models.Model):

    panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):

    panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
    reg_id = models.CharField(max_length=20)
    to = models.CharField(max_length=200)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:40]