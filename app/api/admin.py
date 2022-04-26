from django.contrib import admin
from api import models


admin.site.register(models.Database)
admin.site.register(models.Resource)
admin.site.register(models.Item)
