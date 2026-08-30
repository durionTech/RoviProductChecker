from django.db import models
from django.contrib.auth.models import User


class Inspection(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('PASS', 'Pass'),
        ('FAIL', 'Fail'),
        ('ERROR', 'Error'),
    ]

    inspector = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    product_name = models.CharField(
        max_length=255,
        blank=True
    )

    front_image = models.ImageField(
        upload_to='inspections/front/'
    )

    back_image = models.ImageField(
        upload_to='inspections/back/',
        blank=True,
        null=True
    )

    side_image = models.ImageField(
        upload_to='inspections/side/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    extracted_mrp = models.CharField(
        max_length=100,
        blank=True
    )

    extracted_net_quantity = models.CharField(
        max_length=100,
        blank=True
    )

    extracted_manufacturer = models.TextField(
        blank=True
    )

    extracted_date = models.CharField(
        max_length=100,
        blank=True
    )

    extracted_text = models.TextField(
        blank=True
    )

    violations = models.JSONField(
        default=list,
        blank=True
    )

    ocr_result = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Inspection #{self.id} - {self.status}"




    


    