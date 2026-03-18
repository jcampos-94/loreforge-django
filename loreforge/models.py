from django.db import models


# Faction model
class Faction(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Character model
class Character(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    faction = models.ForeignKey(
        Faction, on_delete=models.CASCADE, related_name="members"
    )

    mentor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    def __str__(self):
        return self.name
