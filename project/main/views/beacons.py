from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.mixins import ListModelMixin

from main.serializers.beacons_serializer import BeaconsSerializer

from ..models import Beacon
from ..utils.permissions import CustomDjangoModelPermissions


class BeaconsView(ListCreateAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = BeaconsSerializer

    def get_queryset(self):
        queryset = Beacon.objects.all()
        name = self.request.query_params.get('name')
        beacon_id = self.request.query_params.get('beacon_id')

        if name:
            queryset = queryset.filter(name=name)
        elif beacon_id:
            queryset = queryset.filter(beacon_id=beacon_id)

        return queryset


class BeaconsDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = Beacon.objects.all()
    serializer_class = BeaconsSerializer
