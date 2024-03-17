from django.db import models

# Create your models here.

class DeadLetterLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    error = models.CharField(max_length=25000, null=True)
    event = models.CharField(max_length=25000)
    is_retryable = models.BooleanField()
    retries_made = models.IntegerField()
