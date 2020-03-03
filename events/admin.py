from django.contrib import admin
from .models import Event , Ticket, Follow

admin.site.site_header = "Event Booking Dashboard"

class Auth_UserAdmin(admin.ModelAdmin):
    user_list_template = 'admin/user_change_list.html'

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Follow)
