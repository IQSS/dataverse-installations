"""
Purpose: Help optimize read-only pages, especially published Dataverses, until
metadata blocks can be switched to JSON schema.  (And maybe we start using a document db)

To generate/save JSON documents containing core dataset information including:
    - Parent Dataverse info
    - Metadata (all blocks)
    - File listings
May (potentially) be used to:
    - Generate API responses
    - Supply core data to render parts of the dataset landing page
        - e.g. Metadata blocks, file listings
    -
"""
from __future__ import unicode_literals

from collections import OrderedDict
import json

from django.db import models
from django.utils.text import slugify

from dv_apps.datasets.models import Dataset, DatasetVersion

from model_utils.models import TimeStampedModel
from jsonfield import JSONField

class DatasetDoc(TimeStampedModel):
    """Store a JSON representation of a Dataset"""

    name = models.CharField(max_length=255, help_text='Name of the dataset version')

    slug = models.SlugField(max_length=255, help_text='Auto-filld on save.')

    semantic_version = models.CharField(max_length=20, help_text='Auto-filled on save.  Canonical version number.  e.g. 1.0, 1.5, 2.0, 2.4, etc')

    dataset_version = models.ForeignKey(DatasetVersion)

    dset_version_id = models.IntegerField(help_text='Auto-filled on save.'\
        , blank=True, null=True)

    doc = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})


    def __str__(self):
        return self.name

    class Meta:
        pass
        #unique_together = ('schema', 'datafile_id', 'version')
        #ordering = ('schema', '-version',)
        #verbose_name = 'File metadata'
        #verbose_name_plural = 'File metadata'

    def save(self, *args, **kwargs):
        assert self.dataset_version.id is not None,\
            "The Dataset Version MUST be saved before using this object"

        self.semantic_version = self.dataset_version.get_semantic_version()
        self.dset_version_id = self.dataset_version.id
        self.slug = slugify('%s-%s' % (self.name, self.semantic_version))

        super(DataverseDoc, self).save(*args, **kwargs)
