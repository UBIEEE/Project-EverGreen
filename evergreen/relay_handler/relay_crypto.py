import datetime
import secrets

import bcrypt

from relay_handler.models import RelayDevice

# TODO: It would probably be a good idea to add a peppering mechanism


def register_new_relay_device(
    call_name: str,
    vendor: str,
    device_type: str,
    initial_activation: datetime.datetime = datetime.datetime.now(
        datetime.timezone.utc
    ),
    expected_message_interval: datetime.timedelta | None = None,
) -> str:
    """Creates a new RelayDevice in the database.
    Returns the raw password for the RelayDevice which is a url safe string.
    """

    salt: bytes = bcrypt.gensalt()
    password_text: str = secrets.token_urlsafe(nbytes=64)
    password_binary: bytes = password_text.encode(encoding="ascii")
    bcrypted_hash: bytes = bcrypt.hashpw(password=password_binary, salt=salt)

    RelayDevice.objects.create(
        call_name=call_name,
        vendor=vendor,
        device_type=device_type,
        initial_activation_datetime=initial_activation,
        currently_active=True,
        expected_message_interval=expected_message_interval,
        bcrypted_hashed_authentication_token=bcrypted_hash,
    )
    return password_text


def activate_existing_relay_device(call_name: str):
    relay_device: RelayDevice = RelayDevice.objects.get(call_name=call_name)
    relay_device.currently_active = True
    relay_device.save(update_fields=["currently_active"])


def deactivate_existing_relay_device(call_name: str):
    relay_device: RelayDevice = RelayDevice.objects.get(call_name=call_name)
    relay_device.currently_active = False
    relay_device.save(update_fields=["currently_active"])


def validate_raw_auth_token(device: RelayDevice, raw_token_text: str):
    """Checks the auth token for a RelayDevice against the salted and hashed version
    stored in the database.
    Returns true if the token is valid for this RelayDevice AND if the RelayDevice
    is active, and false otherwise.
    """
    inputted_token_binary: bytes = raw_token_text.encode(encoding="ascii")
    validity = bcrypt.checkpw(
        password=inputted_token_binary,
        hashed_password=device.bcrypted_hashed_authentication_token,
    )
    return validity
