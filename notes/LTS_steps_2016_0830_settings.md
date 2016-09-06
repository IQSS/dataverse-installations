
### (1) Copy the settings template

Within the ```miniverse``` project directory, run the following line:

```
cp miniverse/settings/lts_settings_template.py miniverse/settings/lts_settings.py
```

### (2) Manually update the settings in ```lts_settings.py```

1. Set a ```SECRET_KEY```
  - Can generate one using this script: https://gist.github.com/mattseymour/9205591
1. ```SWAGGER_HOST```
  - Make sure this matches the url of the server--without the 'http' or 'https'
    - Example: ```SWAGGER_HOST = 'services.dataverse.harvard.edu'```
1. ```DATABASES```
  - Set the databases location/credentials appropriately
  - ```default``` is a new database for this app
  - ```dataverse``` is the existing dataverse db set to read only
    - Note: Different than the prior instructions, this user ```miniverse_dv_user``` is differentiated from the ```default``` db user.
1. ```ALLOWED_HOSTS```
  - List the urls and IP addresses or the server
  - Example: ```ALLOWED_HOSTS = ('services.dataverse.harvard.edu',
      '52.86.18.14',  # static IP
      )```
1. Mail Settings: ```EMAIL_HOST```, ```EMAIL_PORT```, etc
  - Set these in appropriately to allow the server to send messages to the administrators
1. ```STATIC_ROOT```
  - This is the _destination_ directory for static files.
  - Apache will directly serve content from this directory including css, js, images, and several HTML files
1. ```STATIC_URL```
  - Currently set to ```/static/```, this is the path where ```STATIC_ROOT``` is served from
  - Note: This can also be a fully qualified url.
1. ```MEDIA_ROOT```
  - This is the _destination_ directory for uploaded files and must differ from ```STATIC_ROOT```
  - Apache will serve content from this directory as well as be able to upload to this directory
1. ```MEDIA_URL```
  - Currently set to ```/media/```, this is the path where ```MEDIA_ROOT``` is served from
  - Note: This can also be a fully qualified url.
1. Test database after line: ```if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage```
  - Not sure if this will run in production
  - The db credentials should be allowed to create and destroy a db named ```test_miniverse_default```
    - The naming is automatic: ```test_``` is prepended to ```miniverse_default```

### (3) Command line set-up

 - Create a virtualenv named ```miniverse```
    - Edit the ```postactivate``` file (```/opt/dvn/app/miniverse/.virtualenvs/postactivate```) to have the following contents:

```
#!/bin/bash
# This hook is sourced after every virtualenv is activated.
export DJANGO_SETTINGS_MODULE=miniverse.settings.lts_settings.py
```

 - Invoke the virtualenv
 - Within the main ```miniverse``` directory:
    - Try: ```python manage.py check --settings=miniverse.settings.lts_settings```
 - If the above command works, run the following:

```
python manage.py migrate --settings=miniverse.settings.lts_settings    # creates miniverse tables
python manage.py createsuperuser --settings=miniverse.settings.lts_settings   # create a superuser for yourself
python manage.py collectstatic --settings=miniverse.settings.lts_settings   # collect your static files
```

### (4) Load the map data

 - Copy the ```miniverse/media/logos``` to the directory you set for ```MEDIA_ROOT```/logos
   - You should end up with a new ```logos``` directory under your ```MEDIA_ROOT```
 - Load the logo data to the database:
```
python manage.py loaddata dv_apps/installations/fixtures/installations_2016_0826.json --settings=miniverse.settings.lts_settings
```


### (5) WSGI file to use for new settings

- ```miniverse/wsgi_lts.py```
- Note, with apache, you may need to update this file to invoke the virtualenv
