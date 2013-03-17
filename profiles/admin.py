from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import NotasoUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = NotasoUser
        fields = ('email', 'first_name', 'last_name',
            'facebook_id', 'facebook_name', 'gender', 'raw_data')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NotasoUser

    def clean_password(self):
        # Regardless of what the user provides, return the
        # initial value. This is done here, rather than on
        # the field, because the field does not have access
        # to the initial value
        return self.initial["password"]


class NotasoUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('first_name', 'last_name', 'email',
        'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ('email',)

    fieldsets = (
            (None, {
                'fields': ('first_name', 'last_name', 'email', 'password')}
            ),
            ('Other info', {
                'fields': ('facebook_id', 'facebook_name',
                    'gender', 'raw_data', 'notaso_user_id')}
            ),
            ('Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser',
                    'groups', 'user_permissions')}
            ),
            ('Important dates', {
                'fields': ('last_login',)}
            ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1',
                'password2', 'facebook_id', 'facebook_name',
                'gender', 'raw_data', 'notaso_user_id')}
        ),
    )

admin.site.register(NotasoUser, NotasoUserAdmin)
