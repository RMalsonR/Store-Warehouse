import json
import os
import binascii

import requests
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from Warehouse.settings import STORE_URL
from .enums import Status


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


class Warehouse(models.Model):
    token = models.CharField(max_length=40, verbose_name='Token-key', primary_key=True,
                             default=generate_token(), help_text="Don't touch it :)")
    name = models.CharField(max_length=128, verbose_name='Warehouse Account name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Warehouse account'
        verbose_name_plural = 'Warehouse accounts'


class WarehouseOrder(models.Model):
    # it should be unique unique field
    order_number = models.CharField(max_length=128, verbose_name='Order number (might be text)')
    status = models.CharField(max_length=32, choices=Status.as_choices(), verbose_name='Order status')
    warehouse_account = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name='Warehouse Account')

    class Meta:
        verbose_name = 'Warehouse order'
        verbose_name_plural = 'Warehouse orders'


# Handle pre_save receiver to synchronize with store
@receiver(pre_save, sender=WarehouseOrder)
def pre_save_handler(sender, instance, *args, **kwargs):
    url = os.path.join(STORE_URL, 'syncStore/')
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {
        'warehouse_account': instance.warehouse_account.token,
        'order_number': instance.order_number,
        'status': instance.status,
        'API_CONNECT': True
    }
    url_for_id = os.path.join(url, f'?order_number={instance.order_number}')
    resp_for_id = requests.get(url_for_id)
    if resp_for_id.status_code not in [200, 201]:
        resp_for_id.raise_for_status()
    if not resp_for_id.json():
        raise ValueError(f'Warehouse account does not have the '
                         f'instance with `order_number`: {instance.order_number}')
    resp_data = resp_for_id.json()[0]
    store_order_id = resp_data['id']
    data['id'] = store_order_id
    url += f'{store_order_id}/'
    response = requests.put(url, data=json.dumps(data), headers=headers)
    if response.status_code not in [200, 201]:
        response.raise_for_status()
