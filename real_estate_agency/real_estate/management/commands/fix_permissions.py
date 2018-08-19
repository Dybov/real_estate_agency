from __future__ import unicode_literals, absolute_import, division

import sys

from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.apps import apps
# from django.utils.encoding import smart_text


class Command(BaseCommand):
    help = "Fix permissions and/or contenttypes."

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            dest='execute_all',
            default=False,
            help='Delete all obsolete contentypes and\
permissions and create necessary permissions',
        )
        parser.add_argument(
            '-c',
            '--contenttypes-delete',
            action='store_true',
            dest='delete_contenttypes',
            default=False,
            help='Delete all obsolete contentypes and combined permissions',
        )
        parser.add_argument(
            '-p',
            '--permissions-delete',
            action='store_true',
            dest='delete_permissions',
            default=False,
            help='Delete obsolete permissions',
        )

    def handle(self, *args, **options):
        execute_all = options.get('execute_all')
        delete_contenttypes = options.get('delete_contenttypes')
        delete_permissions = options.get('delete_permissions')

        if execute_all or delete_contenttypes:
            # Next line is realized in contenttypes management.commands:
            self.delete_obsolete_contenttypes_and_permissions(*args, **options)
            # But standart contenttypes management sometimes works with bugs,
            # so custom added here
        if execute_all or delete_permissions:
            self.delete_obsolete_permissions(*args, **options)
        self.create_permissions(*args, **options)

    def create_permissions(self, *args, **options):
        for model in apps.get_models():
            opts = model._meta
            ctype, created = ContentType.objects.get_or_create(
                app_label=opts.app_label,
                model=opts.object_name.lower(),
                # defaults={'name': smart_text(opts.verbose_name_raw)}
            )

            for codename, name in _get_all_permissions(opts):
                p, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=ctype,
                    defaults={'name': name})
                if created:
                    sys.stdout.write('Adding permission {}\n'.format(p))

    def delete_obsolete_contenttypes_and_permissions(self, *args, **options):
        verbosity = options.get('verbosity')
        contenttypes = ContentType.objects.all()
        for contenttype in contenttypes:
            try:
                # Don't use contenttype.get_object_for_this_type()
                # Because it returns ObjectDoesNotExist
                # In both cases model doesn't exist or objects wasn't created
                contenttype.get_all_objects_for_this_type()
            except AttributeError:
                if verbosity > 0:
                    sys.stdout.write(
                        'Deleting contenttype "{name}" - {app}.{mdl}\n'.format(
                            app=contenttype.app_label,
                            mdl=contenttype.model,
                            name=contenttype.name,
                        )
                    )
                obsolete_permissions = contenttype.permission_set.all()
                for perm in obsolete_permissions:
                    if verbosity > 1:
                        sys.stdout.write(
                            'Deleting permission {name} - {codename}\n'.format(
                                codename=perm.codename,
                                name=perm,
                            )
                        )
                contenttype.delete()
                # Permissions will be deleted by CASCADE

    def delete_obsolete_permissions(self, *args, **options):
        import re
        verbosity = options.get('verbosity')
        permissions = Permission.objects.all()
        standart_permission_pattern = re.compile(
            '^(add|change|delete)_(?P<model>.*)$'
        )
        for permission in permissions:
            m = standart_permission_pattern.search(permission.codename)
            if m:
                c_model = permission.content_type.model
                model_name = m.group('model')
                if c_model != model_name:
                    if verbosity > 0:
                        sys.stdout.write(
                            'Deleting permission: {perm}\n'.format(
                                perm=permission,
                            )
                        )
                    permission.delete()
            else:
                if verbosity > 0:
                    sys.stdout.write(
                        'Unknown permission "{name}" - {codename}\n'.format(
                            codename=permission.codename,
                            name=permission,
                        )
                    )
