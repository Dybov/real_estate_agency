from django.shortcuts import render, redirect
from django.contrib.admin.helpers import AdminForm
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm


from .models import RealEstateUser


class ObForm(ModelForm):
    class Meta:
        model = RealEstateUser
        fields = (
            'username', 'last_name', 'first_name', 'patronymic',
            'email', 'phone_number', 'photo', 'bio', 'show_at_company_page')


@login_required
def change_own_profile(request):
    user = request.user

    if request.method == "POST":
        print(request.POST)
        form = ObForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if '_save' in request.POST:
                return redirect('admin:index')
    else:
        form = ObForm(instance=user)

    adminform = AdminForm(
        form,
        [(None, {'fields': form.fields, })],
        {},  # Prepopulated fields
    )
    return render(request, 'accounts/change_profile.html', {
        'user': user,
        'has_permission': True,
        'opts': RealEstateUser._meta,
        'title': 'Изменение профиля',
        'change': False,
        'is_popup': False,
        'save_as': False,
        'has_delete_permission': False,
        'has_add_permission': False,
        'has_change_permission': True,
        'link': user,
        'form': form,
        'adminform': adminform,
    })
