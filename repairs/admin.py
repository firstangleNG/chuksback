from django.contrib import admin
from .models import Property,RepairTicket,Description,Payment


admin.site.register(Property)
admin.site.register(RepairTicket)
admin.site.register(Description)
admin.site.register(Payment)