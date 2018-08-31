from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
    Group,
)
from django.contrib.auth.validators import (
    ASCIIUsernameValidator,
    UnicodeUsernameValidator
)
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from real_estate.models.helper import get_file_path
from real_estate.models.image import spec_factory
from contacts.views import (
    phone_stringify,
    DEFAULT_PHONE,
    DEFAULT_EMAIL,
)


def get_username_validator():
    return UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()


class AbstactRealEstateUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = get_username_validator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer.\
 Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super(AbstactRealEstateUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class RealEstateUser(AbstactRealEstateUser):
    patronymic = models.CharField(_('отчество'), max_length=30, blank=True)
    phone_number = PhoneNumberField(
        _('номер телефона'),
        blank=True,
    )
    show_phone_number = models.BooleanField(
        _('Отображать номер телефона на сайте'),
        default=True,
        help_text=_('Показывать ли личный номер на сайте?\
В противном случае будет показан номер компании')
    )
    show_email = models.BooleanField(
        _('Отображать email на сайте'),
        default=True,
        help_text=_('Показывать ли личный email на сайте?\
В противном случае будет показан email компании')
    )
    photo = models.ImageField(
        verbose_name=_('фото'),
        upload_to=get_file_path,
        help_text=_('Будет отображаться на сайте при определенных настройках'),
        blank=True,
    )
    photo_300x300 = spec_factory(
        300,
        300,
        source='photo',
        to_fit=False,
        options__quality=70,
        format='jpeg',
    )
    photo_370x500 = spec_factory(
        370,
        500,
        source='photo',
        to_fit=False,
        options__quality=80,
        format='jpeg',
    )
    bio = models.TextField(_('биография'), max_length=255, blank=True)
    show_at_company_page = models.BooleanField(
        _('Отображать профиль на сайте'),
        default=True,
        help_text=_('Показывать ли контакт на странице с контактами компании\
 и на прочих страницах, где это уместно?')
    )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name plus patronymic,
        with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        if self.patronymic:
            full_name += ' %s' % self.patronymic
        return full_name.strip()
    get_full_name.short_description = _("Полное имя")

    def get_short_name(self):
        "Returns the short name for the user."
        short_name = '%s %s.' % (
            self.last_name,
            self.first_name[0] if self.first_name else '',
        )
        if self.patronymic:
            short_name += ' %s.' % self.patronymic[0]
        return short_name.strip().title()
    get_short_name.short_description = _("Сокращенное имя")

    def get_phone_number(self):
        if self.phone_number and self.show_phone_number:
            return self.phone_number
        return DEFAULT_PHONE

    def get_phone_number_str(self):
        return phone_stringify(self.get_phone_number())

    def get_photo(self):
        if self.photo:
            return self.photo.url
        return static('img/team/placeholder.jpg')

    def get_agent_photo(self):
        if self.photo:
            return self.photo_300x300.url
        return static('img/team/placeholder_300x300.jpg')

    def get_contact_photo(self):
        if self.photo:
            return self.photo_370x500.url
        return static('img/team/placeholder_370x500.jpg')

    def get_email(self):
        if self.email and self.show_email:
            return self.email
        return DEFAULT_EMAIL

    def get_instance_or_default(self):
        if self.is_active \
                and self.show_at_company_page and not self.is_superuser:
            return self
        default_user_id = getattr(settings, 'DEFAULT_USER_ID', None)
        if default_user_id:
            try:
                default_user = RealEstateUser.objects.get(
                    id=default_user_id,
                    is_active=True,
                    show_at_company_page=True,
                    is_superuser=False)
            except Exception:
                pass
            else:
                return default_user
        user_list = RealEstateUser.objects.filter(
            is_active=True,
            show_at_company_page=True,
            is_superuser=False
        )
        return user_list[0]

    def __str__(self):
        return self.get_short_name()


class RealEstateGroup(Group):
    class Meta:
        proxy = True
        verbose_name = _('группа')
        verbose_name_plural = _('группы')
