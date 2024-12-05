# FIXME: There should be an actual router here that routes different valid requests to their appropriate functions
# For the sake of the demo, we will just use this magic function for now to take care of the image requests from the
# Pi since that is what we know we are getting, and is the only thing we are getting.

from django.http import HttpRequest
from relay_handler.models import RelayDevice, RelayUpload
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File


def handle_timelapse_upload_from_pi(request: HttpRequest, relay_device: RelayDevice):
    if "timelapse" not in request.FILES:
        return
    timelapse_file: UploadedFile = request.FILES["timelapse"]
    try:
        uploading_file: File = File(file=timelapse_file, name=timelapse_file.name)
    except:
        return

    RelayUpload.objects.create(file=uploading_file)
