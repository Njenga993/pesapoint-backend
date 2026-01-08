from django.contrib import admin
from .models import Business, BusinessUser


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(BusinessUser)
class BusinessUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'business', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('user__username', 'business__name')
