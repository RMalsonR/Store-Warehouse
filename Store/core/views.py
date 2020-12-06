from django.db.models.signals import pre_save
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import StoreOrder, pre_save_handler
from .serializers import StoreOrderSerializer


class StoreOrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    serializer_class = StoreOrderSerializer
    queryset = StoreOrder.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['order_number', ]

    # Disconnect receiver for avoid recursive actions using API communication
    def update(self, request, *args, **kwargs):
        if request.data.get('API_CONNECT', False):
            pre_save.disconnect(pre_save_handler, sender=StoreOrder)
            response = super(StoreOrderViewSet, self).update(request, *args, **kwargs)
            pre_save.connect(pre_save_handler, sender=StoreOrder)
        else:
            response = super(StoreOrderViewSet, self).update(request, *args, **kwargs)
        return response
