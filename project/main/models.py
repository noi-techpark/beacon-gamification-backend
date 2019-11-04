from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# For the quest body if we will use postgres
# from django.contrib.postgres.fields import JSONField

# User


class ExtendedUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='extendeduser'
    )
    points = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance)


# Beacon


class Beacon(models.Model):
    name = models.CharField(max_length=100)
    beacon_id = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name + ' || ' + self.beacon_id

# Quest


class Quest(models.Model):
    name = models.CharField(max_length=300)
    position = models.TextField(blank=True)
    description = models.TextField(blank=True)
    epilogue = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.name


class QuestStep(models.Model):
    quest = models.ForeignKey(
        'Quest', related_name='steps', on_delete=models.CASCADE)
    beacon = models.ForeignKey(
        Beacon,
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=300)
    properties = models.TextField(blank=True)
    value_points = models.IntegerField(null=True)
    quest_index = models.IntegerField(null=True)
    type = models.CharField(max_length=20, blank=True)
    instructions = models.TextField()

    def __str__(self):
        return self.name
