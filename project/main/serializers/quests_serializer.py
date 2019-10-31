from rest_framework import serializers

from ..models import Quest, QuestStep


class QuestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestStep
        fields = '__all__'


class QuestSerializerSteps(serializers.ModelSerializer):
    steps = QuestStepSerializer(many=True, required=False)

    class Meta:
        model = Quest
        fields = '__all__'


class QuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quest
        fields = '__all__'
