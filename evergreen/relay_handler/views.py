import bcrypt
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import relay_handler.relay_processor as relay_processor
from relay_handler.models import RelayDevice, RelayUpload

# Create your views here.


# FIXME
@csrf_exempt
def relay_request(request: HttpRequest):
    """Accepts an attempt at a RelayDevice uploading data for the server to process.
    This has to be csrf_exempt because the RelayDevice's will not be able to get a csrf
    token from the server since they never actually access the webpage.
    Authentication is done solely based on authentication tokens placed in the device,
    which it uploads with all of its requests to the server."""
    if request.method != "POST":
        return HttpResponseBadRequest()

    # bail on this request early if it doesn't have what we want
    if "Call-Name" not in request.POST or "Relay-Device-Auth-Token" not in request.POST:
        return HttpResponseBadRequest()

    received_call_name: str = request.POST["Call-Name"]
    try:
        relay_device: RelayDevice = RelayDevice.objects.get(
            call_name=received_call_name
        )
    except Exception:
        return HttpResponseBadRequest()

    received_auth_token_string: str = request.POST["Relay-Device-Auth-Token"]
    received_auth_token_binary: bytes = received_auth_token_string.encode(
        encoding="ascii"
    )

    if bcrypt.checkpw(
        received_auth_token_binary, relay_device.bcrypted_hashed_authentication_token
    ):
        # process data here
        if relay_processor.handle_time_lapse_upload_from_pi(
            request=request, relay_device=relay_device
        ):
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest("Failed to store. ")

    return HttpResponseBadRequest()


# FIXME
@login_required()
def view_time_lapse(request: HttpRequest):
    """Returns the time lapse .mp4 file."""
    relay_upload = (
        RelayUpload.objects.latest()
    )  # FIXME: not general, will only work when there is a single RelayDevice!
    return FileResponse(relay_upload.file.chunks())
