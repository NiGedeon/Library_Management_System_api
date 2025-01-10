from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Book, Transaction

# Custom admin configuration for the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Fields displayed in the admin user list
    list_display = ('username', 'email', 'date_of_membership', 'active_status', 'is_staff', 'is_superuser')
    list_filter = ('active_status', 'is_staff', 'is_superuser', 'date_of_membership')
    search_fields = ('username', 'email')
    ordering = ('-date_of_membership',)
    filter_horizontal = ('groups', 'user_permissions') 

    # Fields for viewing/editing a user in detail
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('date_of_membership', 'active_status')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    # Fields for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'active_status', 'is_staff', 'is_superuser'),
        }),
    )

# Custom admin configuration for the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'published_date', 'copies_available')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'author', 'isbn')
    ordering = ('-published_date',)

# Custom admin configuration for the Transaction model
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'returned_date')
    list_filter = ('borrowed_date', 'returned_date')
    search_fields = ('user__username', 'book__title')
    ordering = ('-borrowed_date',)
    raw_id_fields = ('user', 'book')  # Optimizes queries for ForeignKey fields
