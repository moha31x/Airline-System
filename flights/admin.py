"""This script defines adminstrative tasks."""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User, Passenger, Flight, Staff


class UserCreationForm(forms.ModelForm):
    """class object to generate user creation forms."""
    class Meta:
        """class"""
        model = User
        fields = ('username', 'email', 'user_type')

        def save(self, commit=True):
            # Save the provided password in hashed format
            user = super().UserCreationForm().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user


class CustomUserAdmin(UserAdmin):
    """class to create user creation forms."""
    # The forms to add and change user instances
    add_form = UserCreationForm
    # fields to display in admin page while viewing all users
    list_display = ('username', 'email', 'user_type')
    # order in which displayed
    ordering = ["email"]

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password', 'first_name', 'last_name',
                'is_superuser', 'is_staff', 'is_active', 'user_type'
            )}
        ),
    )

    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)#, UsersAdmin)
admin.site.register(Passenger)
admin.site.register(Flight)
admin.site.register(Staff)
