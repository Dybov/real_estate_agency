import os

from django.conf import settings
from django.core.checks import Warning, register
from django.db import models
from django.utils.translation import ugettext as _

from imagekit import ImageSpec
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from PIL import Image, ImageEnhance

from .helper import get_file_path

# opacity ratio from 0 to 1
BASE_OPACITY = 0.7
# size ratio from 0 to 1, where 1 = image.size
BASE_WATERMARK_SIZE_RATIO = 0.3
# c, l, r, t, b - center, left, right, top, bottom
# allowed values: c, l, r, t, b, tl, bl, tr, br
BASE_WATERMARK_POSITION = 'bl'

_watermark_path = settings.WATERMARK_IMAGE_PATH


@register()
def example_check(*args, **kwargs):
    warnings = []
    if not _watermark_path or not os.path.exists(_watermark_path):
        warnings.append(
            Warning(
                "settings.WATERMARK_IMAGE_PATH isn't defined",
                hint="Please set correct image path otherwise \
watermark won't be overlay. Don't forget to set it for production too!",
                id='real_estate.models.image.W001',
            )
        )
    return warnings


class Opacity(object):
    """Add opacity to spec image with value of opacity"""

    def __init__(self, opacity):
        self.opacity = opacity

    def add_opacity(self, im):
        assert self.opacity >= 0 and self.opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
        im.putalpha(alpha)
        return im

    def process(self, img):
        return self.add_opacity(img)


class Watermark(ImageSpec):
    opacity = BASE_OPACITY
    processors = [
        Opacity(opacity),
    ]
    format = 'PNG'


if _watermark_path and os.path.exists(_watermark_path):
    source_file = open(_watermark_path, 'rb')

    watermark_generator = Watermark(source=source_file)
    WATERMARK_SPEC = watermark_generator.generate()
    source_file.close()
else:
    WATERMARK_SPEC = None


def spec_factory(
    width=16, height=16, source='image', to_fit=True, *args, **kwargs
):
    """ Abstract factory for ImageSpecField with default thumbnail params"""
    if to_fit:
        main_processor = ResizeToFit(
            width,
            height,
            mat_color=(255, 255, 255, 0)
        )
    else:
        main_processor = ResizeToFill(
            width,
            height,
        )
    processors = kwargs.pop('pre_processors', []) \
        + [main_processor] + kwargs.pop('extra_processors', [])
    return ImageSpecField(
        processors=processors,
        source=source,
        format=kwargs.pop('format', 'PNG'),
        options={
            'quality': kwargs.pop('options__quality', 50),
            'progressive': kwargs.pop('options__progressive', True),
        }
    )


thumbnail_16_16 = spec_factory()
thumbnail_32_32 = spec_factory(32, 32)
thumbnail_64_64 = spec_factory(64, 64)
thumbnail_120_120 = spec_factory(120, 120)
thumbnail_260_260 = spec_factory(260, 260)


def get_position_by_shortcut(shortcut, base_size, overlay_size):
    """ returns tuple (x, y) to paste overlay_size into base_size image by shortcut
    for example BaseImage.paste(OverlayImage, (x, y))
    allowed shortcuts:
    c - center
    l - left
    r - right
    t - top
    b - bottom
    and combinations lt, tl, lb, bl, rt, tr, rb, br
    """
    w, h = base_size
    w_o, h_o = overlay_size

    positions = {}
    c = (int(w / 2) - int(w_o / 2), int(h / 2) - int(h_o / 2))
    positions['c'] = c
    positions['l'] = (0, c[1])
    positions['r'] = (w - w_o, c[1])
    positions['t'] = (c[0], 0)
    positions['b'] = (c[0], h - h_o)

    # For combinations of left/rigth and top/bottom
    for x in ('l', 'r'):
        for y in ('t', 'b'):
            positions[x + y] = (positions[x][0], positions[y][1])
            positions[y + x] = positions[x + y]

    position = positions.get(shortcut)
    if not position:
        raise Exception('Ambiguous shortcut for position - %s' % shortcut)
    return position


def add_watermark(image, wmk_image, size_ratio, pos):
    width, height = image.size
    w_width, w_height = wmk_image.size

    scale = min(
        width / (w_width),
        height / (w_height)
    )
    new_size = (
        int(w_width * scale * size_ratio),
        int(w_height * scale * size_ratio),
    )

    tranparent = Image.new('RGBA', (width, height), (255, 255, 255, 0))

    watermark = wmk_image.resize(new_size)

    tranparent = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    tranparent.paste(image, (0, 0))

    new_pos = get_position_by_shortcut(pos, (width, height), new_size)
    tranparent.paste(watermark, new_pos, mask=watermark)
    return tranparent


class BasePropertyImage(models.Model):
    """Abstract model for all real estate pictures
    Helps to use django inlines with pictures.
    """
    image = models.ImageField(verbose_name=_('изображение'),
                              upload_to=get_file_path)
    thumbnail_admin = spec_factory(100, 100)

    def __str__(self):
        return _('изображение')

    class Meta:
        abstract = True
        verbose_name = _('изображение')
        verbose_name_plural = _('изображения')


class BaseDraggapbleImage(BasePropertyImage):
    """Abstract model for all real estate pictures with ordering
    Helps to use django inlines with pictures.
    """
    position = models.PositiveIntegerField(
        verbose_name=_('позиция'),
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True
        ordering = ('position',)

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.position is None:
            # Append
            try:
                last = model.objects.order_by('-position')[0]
                self.position = last.position + 1
            except IndexError:
                # First row
                self.position = 0

        return super(BaseDraggapbleImage, self).save(*args, **kwargs)


class BaseWatermarkProcessor(object):
    watermark = WATERMARK_SPEC
    # size ratio from 0 to 1, where 1 = image.size
    size = BASE_WATERMARK_SIZE_RATIO
    # c, l, r, t, b - center, left, right, top, bottom
    # allowed values: c, l, r, t, b, lt, lb, rt, rb
    position = BASE_WATERMARK_POSITION

    def process(self, image):
        if not self.watermark:
            return image

        watermark_image = Image.open(WATERMARK_SPEC)
        return add_watermark(
            image,
            watermark_image,
            self.size,
            self.position,
        )
