from django.contrib import admin

from .models import DumpTruck, Stock, UnloadingEvent

admin.site.register(DumpTruck)
admin.site.register(Stock)
admin.site.register(UnloadingEvent)
