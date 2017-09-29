from django.core.urlresolvers import reverse

def htmltag_a(_link, verbose_name, _class=''):
	return "<a href='{_link}' class='{_class}'>{verbose_name}</a>".format(
		_link=_link, 
		verbose_name=verbose_name, 
		_class=_class)

def admin_change_model(model):
	if model:
		__app = model._meta.app_label
		__model = model._meta.model_name
		__id    = model.id
		__link  = reverse('admin:%s_%s_change' % (__app,__model), args=(__id,))
		return htmltag_a(__link, model)