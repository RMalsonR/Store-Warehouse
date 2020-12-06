from django.db.models.signals import pre_save
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import WarehouseOrder, Warehouse, pre_save_handler
from .seralizers import WarehouseOrderSerializer, WarehouseSerializer


class WarehouseOrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    serializer_class = WarehouseOrderSerializer
    queryset = WarehouseOrder.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['order_number', ]

    # Disconnect receiver for avoid recursive actions using API communication
    def create(self, request, *args, **kwargs):
        if request.data.get('API_CONNECT', False):
            pre_save.disconnect(pre_save_handler, sender=WarehouseOrder)
            response = super(WarehouseOrderViewSet, self).create(request, *args, **kwargs)
            pre_save.connect(pre_save_handler, sender=WarehouseOrder)
        else:
            response = super(WarehouseOrderViewSet, self).create(request, *args, **kwargs)
        return response

    def update(self, request, *args, **kwargs):
        if request.data.get('API_CONNECT', False):
            pre_save.disconnect(pre_save_handler, sender=WarehouseOrder)
            response = super(WarehouseOrderViewSet, self).update(request, *args, **kwargs)
            pre_save.connect(pre_save_handler, sender=WarehouseOrder)
        else:
            response = super(WarehouseOrderViewSet, self).update(request, *args, **kwargs)
        return response


class WarehousesListAPIView(ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
