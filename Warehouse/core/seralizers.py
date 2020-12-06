from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from .models import Warehouse, WarehouseOrder


class WarehouseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """
        Object instance -> List of primitive data types.
        """
        ret = list()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret.append(None)
            else:
                ret.append(field.to_representation(attribute))

        return ret

    class Meta:
        model = Warehouse
        fields = '__all__'


class WarehouseOrderSerializer(serializers.ModelSerializer):
    warehouse_account = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())

    class Meta:
        model = WarehouseOrder
        fields = '__all__'
