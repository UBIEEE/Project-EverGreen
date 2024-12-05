from django.db import models
import uuid


# Create your models here.
class RelayDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    call_name = models.CharField(
        db_index=True, blank=False, unique=True, max_length=128
    )  # basically this specific device's username

    vendor = models.CharField(null=True)
    device_type = models.CharField(null=True)

    initial_activation_datetime = models.DateTimeField()
    currently_active = models.BooleanField()
    expected_message_interval = models.DurationField(null=True)

    bcrypted_hashed_authentication_token = models.BinaryField(
        max_length=128
    )  # max length of bytes


class RelayUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    file = models.FileField(upload_to="relay_upload")
    device = models.ForeignKey(RelayDevice, on_delete=models.PROTECT)
    datetime_uploaded = models.DateTimeField()
    description = models.CharField(max_length=512, blank=True)
