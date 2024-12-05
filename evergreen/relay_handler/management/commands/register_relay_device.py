from django.core.management.base import BaseCommand, CommandError
from relay_handler.relay_crypto import register_new_relay_device


class Command(BaseCommand):
    help = "Register a new RelayDevice and return the plaintext password. "

    def add_arguments(self, parser):
        parser.add_argument("call_name", type=str)
        parser.add_argument("vendor", type=str)
        parser.add_argument("device_type", type=str)

    def handle(self, *args, **options):
        call_name: str = str(args[0])
        vendor: str = str(args[1])
        device_type: str = str(args[2])
        password = register_new_relay_device(
            call_name=call_name, vendor=vendor, device_type=device_type
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully registered {call_name}. Password is: {password}. "
            )
        )
