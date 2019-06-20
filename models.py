from __future__ import unicode_literals
from collections import OrderedDict

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.db import models
from decimal import Decimal

# Create your models here.
@python_2_unicode_compatible
class Installation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False, help_text="Needs be active to show on dataverse.org map")
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0000'))
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0000'))
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    marker = models.ImageField(upload_to='logos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True, help_text='auto-filled on save')
    version = models.CharField(max_length=6, blank=True, help_text='Dataversion version.  e.g. "4.3", "3.6.2", etc')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        super(Installation, self).save(*args, **kwargs)

    def view_logo_100(self):
        #return self.logo.url
        if self.logo:
            return self.view_logo(force_width=100)
        return 'n/a'
    view_logo_100.allow_tags=True

    def view_marker(self):
        #return self.logo.url
        if self.marker:
            im = '<img src="%s" />' % (self.marker.url)
            return im
        return 'n/a'
    view_marker.allow_tags=True

    def view_logo(self, force_width=None):
        #return self.logo.url
        if self.logo:
            if force_width:
                im = ('<img src="{0}" width="{1}"/ >'
                    '<br />(width forced to {1}px)').format(\
                        self.logo.url, force_width)
                return im
            else:
                im = '<img src="%s" />' % (self.logo.url)
                return im
        return 'n/a'
    view_logo.allow_tags=True

    def to_json(self, as_string=False, pretty=False):
        """Returns an OrderedDict of the installation attributes"""
        od = OrderedDict()

        od['id'] = self.id
        od['name'] = self.name
        od['full_name'] = self.full_name
        od['is_active'] = self.is_active
        od['description'] = self.description
        od['lat'] = self.lat
        od['lng'] = self.lng

        od['logo'] = '%s://%s%s' % (settings.SWAGGER_SCHEME,
                                    settings.SWAGGER_HOST,
                                    self.logo.url)
        #marker = self.marker
        od['url'] = self.url
        od['slug'] = self.slug
        od['version'] = self.version if self.version else None
        return od



@python_2_unicode_compatible
class Institution(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=False, default=Decimal('0.0000'))
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=False, default=Decimal('0.0000'))
    host = models.ForeignKey(
        Installation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name
