from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Train, Booking

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

class TrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'destination', 'total_seats', 'available_seats', 'created_at')
    list_filter = ('source', 'destination')
    search_fields = ('source', 'destination')
    readonly_fields = ('available_seats', 'created_at')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('source', 'destination', 'total_seats')
        }),
        ('Status', {
            'fields': ('available_seats', 'created_at')
        }),
    )

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'train_details', 'booked_at')
    list_filter = ('booked_at',)
    search_fields = ('user__username', 'train__source', 'train__destination')
    ordering = ('-booked_at',)

    def train_details(self, obj):
        return f"{obj.train.source} to {obj.train.destination} (Train ID: {obj.train.id})"
    train_details.short_description = 'Train Route'

    fieldsets = (
        (None, {
            'fields': ('user', 'train')
        }),
        ('Booking Info', {
            'fields': ('booked_at',)
        }),
    )
    readonly_fields = ('booked_at',)

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(Booking, BookingAdmin)