from django.contrib import admin
from users.models import Member, Author
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = Member
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('membership_date', 'last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

    search_fields = ('email', )
    ordering = ('email',)

admin.site.register(Member, CustomUserAdmin)
admin.site.register(Author)