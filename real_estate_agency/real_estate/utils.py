from django.core.urlresolvers import reverse


def htmltag_a(_link, verbose_name, _class=''):
    return "<a href='{_link}' class='{_class}'>{verbose_name}</a>".format(
        _link=_link,
        verbose_name=verbose_name,
        _class=_class
    )


def admin_change_model(model):
    if model:
        __app = model._meta.app_label
        __model = model._meta.model_name
        __id = model.id
        __link = reverse('admin:%s_%s_change' % (__app, __model), arg=(__id,))
        return htmltag_a(__link, model)


def reorder(apps, schema_editor, app_name, model_name):
    """Fill the position field for draggable models based on their id.
    Filling is important to save integrity
    Use as:
    model_reorder = lambda a, s: reorder(a, s, 'app_name', 'model_name')"""
    Draggable = apps.get_model(app_name, model_name)
    for _object in Draggable.objects.all():
        _object.position = _object.id
        _object.save()
