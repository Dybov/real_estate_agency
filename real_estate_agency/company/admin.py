from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from imagekit.admin import AdminThumbnail
from adminsortable2.admin import SortableAdminMixin

from .models import Award, BankPartner


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        widgets = {
            'image': forms.widgets.ClearableFileInput(attrs={'multiple': True})
        }
        fields = '__all__'


@admin.register(Award)
class AwardAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = AwardForm
    thumb = AdminThumbnail(
        image_field='thumbnail_admin',
        template='admin/display_link_thumbnail.html',
    )
    thumb.short_description = _('миниатюра')

    list_display = ['thumb', ]
    fields = ('image',)

    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('image')
        obj.image = files.pop(0)
        super().save_model(request, obj, form, change)
        for afile in files:
            self.model.objects.create(image=afile)


@admin.register(BankPartner)
class BankPartnerAdmin(SortableAdminMixin, admin.ModelAdmin):
    thumb = AdminThumbnail(image_field='thumbnail_64_64')
    thumb.short_description = _('миниатюра')

    list_display_links = ('title',)
    list_display = ('title', 'thumb')
    fields = ('title', 'image',)
