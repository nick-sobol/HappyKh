"""Creation model for place and addresses"""
import logging
from django.db import models
from users.models import User
from stdimage import models as std_models
from utils import make_upload_image

LOGGER = logging.getLogger('happy_logger')


class Address(models.Model):
    """Addresses model"""
    latitude = models.DecimalField(max_digits=7, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    address = models.CharField(max_length=255, blank=False, default=None)


class Place(models.Model):

    """
    Place model for creation new places
    """

    large = 'large'
    thumbnail = 'thumbnail'
    medium = 'medium'

    VARIATIONS_LOGO = {
        large: (600, 400, True),
        thumbnail: (100, 100, True),
        medium: (300, 200, True),
    }

    def _make_upload_logo(serl, filename):
        """
        Function which creates path for place's logo.
        Should be used as base-function for function in parameter upload_to of
        ImageField.

        :param filename: name of the user's file, ex. 'image.png'
        :return: path to image or None if filename is empty
        """

        return make_upload_image(filename, 'place/logo')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = std_models.StdImageField(
        upload_to=_make_upload_logo,
        blank=True,
        null=True,
        default='',
        variations=VARIATIONS_LOGO,
    )

    @staticmethod
    def get_place(place_id):
        try:
            return Place.objects.get(pk=place_id)
        except Place.DoesNotExist: #pylint: disable = no-member
            LOGGER.error(
                f'Can`t get place because of invalid id,'
                f' place_id: {place_id}'
            )
            return None

    def __str__(self):
        return self.name
