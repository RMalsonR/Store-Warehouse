from django.contrib import admin

from .models import Warehouse, WarehouseOrder


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    readonly_fields = ['token', ]

    # Disable delete operation using django admin
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WarehouseOrder)
class WarehouseOrderAdmin(admin.ModelAdmin):
    # Disable add operation using django admin. Adding orders only from Store throw API
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
