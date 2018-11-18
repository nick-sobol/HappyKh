"""Creation model for place and addresses"""
import logging
from django.db import models
from django.utils import timezone
from stdimage import models as std_models
from users.models import (User, CommentAbstract)
from utils import make_media_file_path

LOGGER = logging.getLogger('happy_logger')


class Address(models.Model):
    """Addresses model"""
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255, blank=False, default=None)

    def __str__(self):
        return self.address


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

    def _make_upload_logo(self, filename):
        """
        Function which creates path for place's logo.
        Should be used as base-function for function in parameter upload_to of
        ImageField.

        :param filename: name of the user's file, ex. 'image.png'
        :return: path to image or None if filename is empty
        """

        return make_media_file_path(
            model_name='Place',
            attr_name='logo',
            original_filename=filename
        )

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
    created = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return self.name


class CommentPlace(CommentAbstract):
    """
    Class which adds ForeignKey to the Place for which
    standard comment was created.
    """
    place = models.ForeignKey(Place, on_delete=models.CASCADE)


class PlaceRating(models.Model):
    """
    Create model for place rating
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    rating = models.FloatField(blank=False)

    def __str__(self):
        return self.place.name