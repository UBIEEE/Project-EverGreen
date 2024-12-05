from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from relay_handler.models import RelayDevice
import bcrypt

# Create your views here.


@csrf_exempt
def relay_request(request: HttpRequest):
    """Accepts an attempt at a RelayDevice uploading data for the server to process.
    This has to be csrf_exempt because the RelayDevice's will not be able to get a csrf
    token from the server since they never actually access the webpage. Authentication is
    done solely based on authentication tokens placed in the device, which it uploads with all
    of its requests to the server."""

    if request.method != "POST":
        return HttpResponseBadRequest()

    if (
        "Call-Name" not in request.headers
        or "Relay-Device-Auth-Token" not in request.headers
    ):
        return HttpResponseBadRequest()

    received_call_name: str = request.headers["Call-Name"]

    try:
        relay_device: RelayDevice = RelayDevice.objects.get(
            call_name=received_call_name
        )
    except:
        return HttpResponseBadRequest()

    received_auth_token_string: str = request.headers["Relay-Device-Auth-Token"]
    received_auth_token_binary: bytes = received_auth_token_string.encode(
        encoding="ascii"
    )

    if bcrypt.checkpw(
        received_auth_token_binary, relay_device.bcrypted_hashed_authentication_token
    ):
        # process data here
        return HttpResponse(status=204)

    return HttpResponseBadRequest()
