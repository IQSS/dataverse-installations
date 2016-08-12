from django.test import TestCase
from dv_apps.terms_of_use.models import TermsOfUseAndAccess

class TermsOfUseTestCase(TestCase):

    #fixtures = ['test_schemas.json']

    def setUp(self):
        pass
        #print ('count: ', MetadataSchema.objects.all().count())
        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    def test_01_toa(self):
        """Test to see if db created"""

        num_toa = TermsOfUseAndAccess.objects.all().count()
        print 'num_toa', num_toa
        self.assertEqual(num_toa, 0)

        #for toa in TermsOfUseAndAccess.objects.all():
            #valid, msg = validate_schema(mschema.schema)
            #self.assertEqual(valid, True)

            # validate schema as JSON string
            #valid2, msg2 = validate_schema_string(mschema.as_json())
            #self.assertEqual(valid2, True)
