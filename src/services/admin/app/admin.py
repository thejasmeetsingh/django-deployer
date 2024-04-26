from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

from app.models import DeploymentPlan


admin.site.site_header = 'Django Deployer Admin'
admin.site.site_title = 'Django Deployer'
admin.site.site_url = None

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    readonly_fields = ('last_login', 'date_joined')


@admin.register(DeploymentPlan)
class DeploymentPlanAdmin(admin.ModelAdmin):
    list_display = ('plan',)
