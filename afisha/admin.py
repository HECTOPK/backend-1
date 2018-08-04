from django.contrib import admin
from afisha.models import Bitcoin

class BitcoinAdmin(admin.ModelAdmin):
    list_display = ("total", "blocks")

admin.site.register(Bitcoin, BitcoinAdmin)
