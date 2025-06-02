from django.core.management.base import BaseCommand, CommandError

from relay_handler.relay_crypto import deactivate_existing_relay_device


class Command(BaseCommand):
    help = "De-active a relay device. Attempted uploads from this device will be refused after this operation. "  # noqa: E501

    def add_arguments(self, parser):
        parser.add_argument("call_name", type=str)

    def handle(self, *args, **options):
        call_name: str = str(options["call_name"])

        try:
            deactivate_existing_relay_device(call_name=call_name)
        except Exception as e:
            raise CommandError(
                f"Error encountered when trying to de-activate device: {e}."
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully de-activated device '{call_name}'. ")
        )
