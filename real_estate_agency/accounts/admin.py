from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _

from applications.forms import RussianPhoneNumberFormMixin

from .models import RealEstateUser, RealEstateGroup


class RealEstateUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = RealEstateUser
        fields = ("username", "email", "phone_number", "photo")


class RealEstateUserForm(RussianPhoneNumberFormMixin, UserChangeForm):
    PHONE_NUMBER_FIELD = 'phone_number'

    class Meta:
        fields = '__all__'
        model = RealEstateUser


class RealEstateUserAdmin(UserAdmin):
    form = RealEstateUserForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'patronymic',
            'email', 'phone_number',
            'photo', 'bio',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'show_at_company_page',
            'groups',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined', )
    list_display = (
        'username', 'get_short_name', 'email', 'phone_number', 'is_active', )
    list_filter = ('is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups',)

    add_form = RealEstateUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2',
                "email", "phone_number", "photo",),
        }),
    )

    def get_queryset(self, request):
        """ Excludes superusers from not superusers querysets"""
        qs = super(RealEstateUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(is_superuser=True)


class RealEstateGroupAdmin(GroupAdmin):
    model = RealEstateGroup

    def get_form(self, request, obj=None, **kwargs):
        form = super(RealEstateGroupAdmin, self).get_form(
            request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields[
                'permissions'
            ].queryset = Permission.objects.exclude(
                content_type__app_label__in=(
                    'auth', 'admin', 'contenttypes',
                    'django_celery_beat', 'sessions',
                ),
            )
        return form


admin.site.register(RealEstateUser, RealEstateUserAdmin)
admin.site.unregister(Group)
admin.site.register(RealEstateGroup, RealEstateGroupAdmin)
