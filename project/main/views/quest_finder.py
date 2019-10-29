from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.models import Beacon, QuestStep, Quest
from main.serializers import beacons_serializer, quests_serializer


class QuestFinderView(APIView):
    def get(self, request):
        beacon_id = ''
        if not request.query_params.get('beacon_id', None):
            return Response(data="Missing beacon_id", status=status.HTTP_400_BAD_REQUEST)

        beacon_id = request.query_params['beacon_id']
        beacon = Beacon.objects.get(beacon_id=beacon_id)
        serialized_beacon = beacons_serializer.BeaconsSerializer(beacon)

        steps = QuestStep.objects.filter(beacon__id=beacon.pk)
        serialized_steps = quests_serializer.QuestStepSerializer(
            steps, many=True)

        quests_id_list = []
        for step in serialized_steps.data:
            quests_id_list.append(step['quest'])

        quests = Quest.objects.filter(pk__in=quests_id_list)
        serialized_quests = quests_serializer.QuestSerializer(
            quests, many=True)

        return Response({"beacon": serialized_beacon.data, 'quests': serialized_quests.data})
