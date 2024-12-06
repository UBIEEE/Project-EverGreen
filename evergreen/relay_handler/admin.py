from django.contrib import admin

import relay_handler.models as models

# Register your models here.
admin.site.register(models.RelayDevice)
admin.site.register(models.RelayUpload)
