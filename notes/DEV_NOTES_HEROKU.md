## deployment

+-- miniverse  
    +-- settings
        +-- heroku_dev.py
    +-- wsgi.py
    +-- urls_heroku_dev.py  (not yet created)
+-- Procfile

# checklist

- [ ] python runtime
    - do we want to go live with 3.x?
- [ ] static files
- [ ] database
  - [ ] database routing
- [ ] secret key


# config vars

  - https://devcenter.heroku.com/articles/config-vars#add-ons-and-config-vars

## Set python version

  - reference: https://devcenter.heroku.com/articles/python-support#supported-python-runtimes

  - location: ```+-- runtime.txt```

```
cat runtime.txt
python-2.7.11
```


## set django vars

- DJANGO_SETTINGS_MODULE
  - set the var:  ```heroku config:set DJANGO_SETTINGS_MODULE=miniverse.settings.heroku_dev```

- SECRET_KEY
  - create a key: https://gist.github.com/joshsee/8c495c2da9b423d42e8d
  - set the key:  ```heroku config:set SECRET_KEY=[key from above]```

## IP info


Name:	demo.dataverse.org
Address: 140.247.115.242

Heroku static IPs:
  - 52.86.18.14
  - 50.17.160.202

Issues:
  - No routing on pages: https://services-dataverse.herokuapp.com/metrics/v1/files/count
  - Not routing on commands:
    - heroku run bin/qgsocksify python manage.py dbshell


## To fix: Site matching query does not exist.

This happens when the db doesn't have an entry for Site with id of 1.

1. Open the shell: ```heroku run python manage.py shell```
2. Add a Site object:
```
# import the Site object
#
from django.contrib.sites.models import Site
from django.conf import settings

# make sure there isn't a Site--should give an error ending with:
# "DoesNotExist: Site matching query does not exist."
#
my_site = Site.objects.get(pk=1)

# Clear any existing sites.  In case Site exists but with wrong pk
#
Site.objects.all().delete()


# Now really make a site
#
site = Site()
site.id = settings.SITE_ID
site.domain = 'services-dataverse.herokuapp.com'
site.name = 'services-dataverse.herokuapp.com'
site.save()

# ensure it exists - shouldn't be an error
my_site = Site.objects.get(pk=1)

```

### email test

```
heroku run python manage.py shell

from django.core.mail import send_mail

to_mail = 'raman_prasad@harvard.edu'
send_mail(
    'Heroku dev - django server',
    'We seem to have contact...',
    'iqss.contact@gmail.com',
    [to_mail],
    fail_silently=False,
)
```

```
import requests
my_referer = 'http://www.w3.org/hypertext/DataSources/Overview.html'
url = 'https://services-dataverse.herokuapp.com/metrics/test-404'
s = requests.Session()
s.headers.update({'referer': my_referer})
s.get(url)
```
