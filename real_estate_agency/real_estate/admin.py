import re

from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from django.utils.text import mark_safe

from imagekit.admin import AdminThumbnail


class DontShowInAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        return {}


class ReadOnlyAdminMixin(object):
    """Disables all editing capabilities."""
    change_form_template = "admin/view.html"

    def __init__(self, *args, **kwargs):
        super(ReadOnlyAdminMixin, self).__init__(*args, **kwargs)
        self.readonly_fields = [f.name for f in self.model._meta.get_fields()]

    def get_actions(self, request):
        actions = super(ReadOnlyAdminMixin, self).get_actions(request)
        del actions["delete_selected"]
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass


class MultiuploadInlinesContainerMixin(object):
    related_filefield_name = 'file|image'
    related_inline_field = 'photos'
    related_inline_form = None
    related_inline_fk = ''
    image_inline_pattern = re.compile(
        '^%s-\d+-(?P<filefield>%s)$' % (
            related_inline_field,
            related_filefield_name,
        ))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        for i in request.FILES:
            # only for appropriate formsets:
            m = self.image_inline_pattern.search(i)
            if m:
                for afile in request.FILES.getlist(i)[:-1]:
                    if not self.related_inline_form:
                        raise MustBeSetError('related_inline_form')

                    if not self.related_inline_fk:
                        raise MustBeSetError('related_inline_fk')

                    filefield = m.group('filefield')
                    file_form = self.related_inline_form(
                        {self.related_inline_fk: obj.id},
                        {filefield: afile},
                    )
                    if file_form.is_valid():
                        file_form.save()
                    else:
                        message_text = _(
                            '<div>Файл "%(file_name)s" не загружен<ul>') \
                            % {'file_name': afile.name}
                        for field, errors in file_form.errors.items():
                            for error in errors:
                                message_text += '<li class="{message_class}">{field}:\
                                 {error}</li>'.format(
                                    field=field,
                                    error=error,
                                    message_class=messages.DEFAULT_TAGS.get(
                                        messages.WARNING),
                                )
                        message_text += "</ul></div>"
                        messages.add_message(
                            request, messages.WARNING, mark_safe(message_text))


class MustBeSetError(Exception):
    """MustBeSetError calls when attribute must be set for class"""
    def __init__(self, arg):
        msg = '"%s" must be set for MultiuploadInlinesContainerMixin' % arg
        super(MustBeSetError, self).__init__(msg)


class AdminInlineImages(object):
    thumbnail = AdminThumbnail(
        image_field='thumbnail_admin',
        template='admin/display_link_thumbnail.html',
    )
    thumbnail.short_description = _('миниатюра')
