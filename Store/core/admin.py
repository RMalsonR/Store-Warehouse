from django.contrib import admin

from .models import StoreOrder


@admin.register(StoreOrder)
class StoreOrderAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
