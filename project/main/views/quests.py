from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from main.serializers import quests_serializer

from ..models import Quest, QuestStep
from ..utils.permissions import CustomDjangoModelPermissions

# QUEST


class QuestListView(ListCreateAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = Quest.objects.all()
    serializer_class = quests_serializer.QuestSerializerSteps


class QuestDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = Quest.objects.all()
    serializer_class = quests_serializer.QuestSerializerSteps


# STEPS


class QuestStepListView(ListCreateAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = QuestStep.objects.all()
    serializer_class = quests_serializer.QuestStepSerializer


class QuestStepDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = QuestStep.objects.all()
    serializer_class = quests_serializer.QuestStepSerializer
