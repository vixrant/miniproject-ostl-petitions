from django.contrib import admin
from . import models

admin.site.register(models.Petition)
admin.site.register(models.Signature)
