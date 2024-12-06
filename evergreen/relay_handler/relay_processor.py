# FIXME: There should be an actual router here that routes different valid requests
# to their appropriate functions.
# For the sake of the demo, we will just use this magic function for now to take care
# of the image requests from the Pi since that is what we know we are getting, and is
# the only thing we are getting.

import datetime

from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest

from relay_handler.models import RelayDevice, RelayUpload


def handle_time_lapse_upload_from_pi(
    request: HttpRequest, relay_device: RelayDevice
) -> bool:
    if len(request.FILES) != 1:
        return False
    time_lapse_file: UploadedFile = list(request.FILES.values())[0]
    # index_of_uploaded_file_in_tuple = 1
    # time_lapse_file: UploadedFile = time_lapse_item[index_of_uploaded_file_in_tuple]
    # TODO: Verify MIME type
    time_lapse_name: str = time_lapse_file.name
    try:
        upload_timestamp = int(request.POST["UNIX-Timestamp"])
        datetime_uploaded: datetime.datetime = datetime.datetime.fromtimestamp(
            upload_timestamp
        )
        uploading_file: File = File(file=time_lapse_file, name=time_lapse_name)
    except Exception:
        return False

    RelayUpload.objects.create(
        file=uploading_file, device=relay_device, datetime_uploaded=datetime_uploaded
    )

    return True
