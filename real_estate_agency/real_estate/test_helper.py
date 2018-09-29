import mock

from django.core.files import File

from address.models import StreetModel, NeighbourhoodModel

IMAGE_COUNTER = 1


def create_mock_image_file(name=None):
    file_mock = mock.MagicMock(spec=File, name='FileMock')
    if not name:
        name = 'test_%s.jpg' % IMAGE_COUNTER
    file_mock.name = name
    return file_mock


def create_neighbourhood(name='neighbourhood'):
    _objects = NeighbourhoodModel.objects.filter(name=name)
    if not _objects:
        return NeighbourhoodModel.objects.create(name=name)
    return _objects[0]


def create_street(name='street'):
    _objects = StreetModel.objects.filter(name=name)
    if not _objects:
        return StreetModel.objects.create(name=name)
    return _objects[0]
