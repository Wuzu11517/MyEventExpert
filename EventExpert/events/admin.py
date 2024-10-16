from django.contrib import admin
from .models import EmailList

@admin.register(EmailList)
class EmailListAdmin(admin.ModelAdmin):
    list_display = ['email', 'added_at']
    search_fields = ['email']
from .models import Event


# Register your models here.
admin.site.register(Event)
