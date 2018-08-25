from django.db import models
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
from django.core.mail import send_mail
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from real_estate.models.helper import get_file_path


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
    photo = models.ImageField(
        verbose_name=_('фото'),
        upload_to=get_file_path,
        help_text=_('Будет отображаться на сайте при определенных настройках'),
        blank=True,
    )
    bio = models.TextField(_('биография'), max_length=255, blank=True)
    show_at_company_page = models.BooleanField(
        _('Отображать на сайте'),
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
            self.first_name[0],
        )
        if self.patronymic:
            short_name += ' %s.' % self.patronymic[0]
        return short_name.strip().title()
    get_short_name.short_description = _("Сокращенное имя")

    def get_phone_number(self):
        return self.phone_number

    def get_photo(self):
        return self.photo

    def __str__(self):
        return self.get_short_name()


class RealEstateGroup(Group):
    class Meta:
        proxy = True
        verbose_name = _('группа')
        verbose_name_plural = _('группы')
