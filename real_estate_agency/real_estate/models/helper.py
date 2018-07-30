def get_file_path(instance, filename):
    """Gets file name for uploaded files
    Specific folder uses app_name, model_name
    Also used uuid number for file_name
    uuid - (https://en.wikipedia.org/wiki/Universally_unique_identifier)
    """
    import uuid
    app = instance._meta.app_label
    model_name = instance._meta.model_name
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'uploads/%s/%s/%s/%s' % (app, model_name, ext, filename)


# Decorator for overriding part of the field in model subclasses
# Source https://stackoverflow.com/questions/927729/\
# how-to-override-the-verbose-name-of-a-superclass-model-field-in-django
def modify_fields(**kwargs):
    def wrap(cls):
        for field, prop_dict in kwargs.items():
            for prop, val in prop_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls
    return wrap
