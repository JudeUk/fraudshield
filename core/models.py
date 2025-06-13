from django.db import models

# Create your models here.

from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Transaction(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    data = models.JSONField()
    score = models.FloatField(null=True)
    flagged = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class ModelInfo(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    model_type = models.CharField(max_length=50)
    trained_at = models.DateTimeField(auto_now_add=True)
    metrics = models.JSONField()
    s3_path = models.CharField(max_length=512)
    is_active = models.BooleanField(default=False)

