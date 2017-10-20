from django.contrib import admin

# Register your models here.


class DontShowInAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        return {}
