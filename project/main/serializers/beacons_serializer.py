from rest_framework import serializers

from main import models


class BeaconsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Beacon
        fields = '__all__'
