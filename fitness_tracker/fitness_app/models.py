from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    muscle_group = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SessionSet(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="sessions")
    performed_at = models.DateField()

    weight = models.FloatField(null=True, blank=True) 
    reps = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.exercise.name} on {self.performed_at}"
