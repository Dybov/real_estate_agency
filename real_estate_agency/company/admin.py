from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Award

from new_buildings.forms import PhotoAdminForm


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        widgets = {'image': forms.widgets.ClearableFileInput(attrs={'multiple': True})}
        fields = '__all__'

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    form = AwardForm
    thumb_width = 300
    thumb_height = 300
    fields = ('image',)

    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist('image')
        # if change:
        obj.image = files.pop(0)
        super().save_model(request, obj, form, change)
        for afile in files:
            self.model.objects.create(image=afile)

    def image_tag(self, obj):
        return format_html('<img src="{url}" height="{height}" />'.format(
                    url=obj.image.url,
                    # width=self.thumb_width,
                    height=self.thumb_height,
                    ))

    image_tag.short_description = 'Image'

    list_display = ['image_tag',]