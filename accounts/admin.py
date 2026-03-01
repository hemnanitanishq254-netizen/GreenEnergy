from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProducerProfile, ConsumerProfile, InvestorProfile


class ProducerProfileInline(admin.StackedInline):
    model = ProducerProfile
    can_delete = False


class ConsumerProfileInline(admin.StackedInline):
    model = ConsumerProfile
    can_delete = False


class InvestorProfileInline(admin.StackedInline):
    model = InvestorProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'city', 'state', 'pincode', 'profile_picture', 'is_verified')
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        inlines = []
        if obj.role == 'producer':
            inlines.append(ProducerProfileInline(self.model, self.admin_site))
        elif obj.role == 'consumer':
            inlines.append(ConsumerProfileInline(self.model, self.admin_site))
        elif obj.role == 'investor':
            inlines.append(InvestorProfileInline(self.model, self.admin_site))
        return inlines


admin.site.register(User, CustomUserAdmin)
admin.site.register(ProducerProfile)
admin.site.register(ConsumerProfile)
admin.site.register(InvestorProfile)