from django.db import models
from django.contrib.admin import TabularInline
from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import TextInput, NumberInput, Textarea
from django.utils.safestring import mark_safe

# it is new sizes for widgets in Inlines
standart_formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size': '10'})},
    models.PositiveSmallIntegerField: {'widget': NumberInput(attrs={'size': '3'})},
    models.IntegerField: {'widget': NumberInput(attrs={'style': 'width:6ch', })},
    models.DecimalField: {'widget': NumberInput(attrs={'style': 'width:12ch', })},
    models.TextField: {'widget': Textarea(attrs={'cols': 1, 'rows': 2})},
}


class AdminImageWidget(AdminFileWidget):
    ''' it base widget which allows to show loaded image near to the 'browse' button '''

    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u'<br><a href="%s" target="_blank"><img src="%s" alt="%s"  width=150/></a><br>' %
                          (image_url, image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class TabularInlineWithImageWidgetInline(TabularInline):
    ''' it is inline which allows to show loaded image near to the 'browse' button into it'''
    # image_fields - fields which images will be shown in admin
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(TabularInlineWithImageWidgetInline, self).formfield_for_dbfield(db_field, **kwargs)
