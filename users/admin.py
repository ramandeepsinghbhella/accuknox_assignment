from django.contrib import admin
from .models import User, FriendRequest

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active')  # Display these fields in the list view
    search_fields = ('email', 'name')  # Add search functionality for these fields
    list_filter = ('is_active',)  # Add filtering by 'is_active' field

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')  # Display these fields in the list view
    list_filter = ('status',)  # Add filtering by 'status' field
    search_fields = ('from_user__email', 'to_user__email')  # Search by users' emails

# Register the models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
