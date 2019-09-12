from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Installation
import json

#class InstallationModelTests(TestCase):
#
#    def test_was_published_recently_with_future_question(self):
#        """
#        was_published_recently() returns False for questions whose pub_date
#        is in the future.
#        """
#        time = timezone.now() + datetime.timedelta(days=30)
#        future_question = Question(pub_date=time)
#        self.assertIs(future_question.was_published_recently(), False)

#def create_question(question_text, days):
#    """
#    Create a question with the given `question_text` and published the
#    given number of `days` offset to now (negative for questions published
#    in the past, positive for questions that have yet to be published).
#    """
#    time = timezone.now() + datetime.timedelta(days=days)
#    return Question.objects.create(question_text=question_text, pub_date=time)

#def create_installation(question_text, days):
def create_installation(name, full_name, is_active, lat, lng, logo, marker, description, url, slug, version):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    #time = timezone.now() + datetime.timedelta(days=days)
    #return Question.objects.create(question_text=question_text, pub_date=time)
    #return Installation.objects.create(name='', full_name='')
    #return Installation.objects.create(name=name, full_name='')
    return Installation.objects.create(name=name,full_name=full_name,is_active=is_active,lat=lat,lng=lng,logo=logo,marker=marker,description=description,url=url,slug=slug,version=version)

class InstallationJsonViewTests(TestCase):
    def test_no_installations(self):
        """
        If no installations exist, the JSON array is empty.
        """
        response = self.client.get('/installations/installations.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"installations": []}')

    def test_create_installation(self):
        """
        The JSON output matches our expectations.
        """
        #create_installation(question_text="Past question.", days=-30)
        #create_installation(name, full_name, is_active, lat, lng, logo, marker, description, url, slug, version)
        # https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
        #image_path='/tmp/cat'
        image_path='/dev/null'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        #create_installation(name="Libra Data",full_name="Libra Data (University of Virginia)",is_active=True,lat=38.034578,lng=-78.507394,logo="",marker="",description="For sharing data.",url="https://dataverse.lib.virginia.edu",slug="",version="")
        create_installation(name="Libra Data",full_name="Libra Data (University of Virginia)",is_active=True,lat=38.034578,lng=-78.507394,logo=image,marker="",description="For sharing data.",url="https://dataverse.lib.virginia.edu",slug="",version="")
        response = self.client.get('/installations/installations.json')
        self.assertEqual(response.status_code, 200)
        first = json.loads(response.content)["installations"][0]
        self.assertEqual(first['name'],'Libra Data')
        self.assertEqual(first['full_name'], 'Libra Data (University of Virginia)')
        self.assertEqual(first['is_active'], True)
        self.assertEqual(first['lat'], 38.034578)
        self.assertEqual(first['lng'], -78.507394)
        # FIXME: better test for logos
        #self.assertEqual(first['logo'], 'https://installations.dataverse.org/media/logos/libra-46x46.jpg')
        self.assertIn('http', first['logo'])
        # TODO: remove marker?
        #self.assertEqual(first['marker'], '')
        self.assertEqual(first['description'], 'For sharing data.')
        self.assertEqual(first['url'], 'https://dataverse.lib.virginia.edu')
        self.assertEqual(first['slug'], 'libra-data')
        self.assertEqual(first['version'], None)

