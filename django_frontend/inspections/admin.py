from django.contrib import admin
from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'product_name',
        'inspector',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'product_name',
        'extracted_mrp',
        'extracted_manufacturer'
    )