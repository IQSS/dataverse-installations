import unittest
from django.test import TestCase
from dv_apps.installations.models import Installation

class InstallationsTestCase(TestCase):

    fixtures = ['installations.json']

    def setUp(self):
        pass
        #print ('count: ', MetadataSchema.objects.all().count())
        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    @unittest.skip("skipping")
    def test_01_toa(self):
        """Test to see if db created"""

        cnt = Installation.objects.all().count()
        self.assertEqual(cnt, 16)
        print 'num installations', cnt
