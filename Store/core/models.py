import os
import json
import requests

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

from Store.settings import WAREHOUSE_URL
from .enums import Status


def get_wh_choices():
    url = os.path.join(WAREHOUSE_URL, 'warehouses/')
    response = requests.get(url, verify=True)
    return response.json()


class StoreOrder(models.Model):
    # it should be unique field
    order_number = models.CharField(max_length=128, verbose_name='Order number (might be text)')
    status = models.CharField(max_length=32, choices=Status.as_choices(), verbose_name='Order status')
    warehouse_account = models.CharField(max_length=40, choices=get_wh_choices(), verbose_name='Warehouse Account')

    class Meta:
        verbose_name = 'Store order'
        verbose_name_plural = 'Store orders'


# Handle pre_save receiver to synchronize with warehouse
@receiver(pre_save, sender=StoreOrder)
def pre_save_handler(sender, instance, *args, **kwargs):
    url = os.path.join(WAREHOUSE_URL, 'syncWH/')
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {
        'warehouse_account': instance.warehouse_account,
        'order_number': instance.order_number,
        'status': instance.status,
        'API_CONNECT': True
    }
    if instance._state.adding is True:
        response = requests.post(url, data=json.dumps(data), headers=headers)
    else:
        url_for_id = os.path.join(url, f'?order_number={instance.order_number}')
        resp_for_id = requests.get(url_for_id)
        if resp_for_id.status_code not in [200, 201]:
            resp_for_id.raise_for_status()
        if not resp_for_id.json():
            raise ValueError(f'Warehouse account does not have the '
                             f'instance with `order_number`: {instance.order_number}')
        resp_data = resp_for_id.json()[0]
        wh_order_id = resp_data['id']
        data['id'] = wh_order_id
        url += f'{wh_order_id}/'
        response = requests.put(url, data=json.dumps(data), headers=headers)
    if response.status_code not in [200, 201]:
        response.raise_for_status()
