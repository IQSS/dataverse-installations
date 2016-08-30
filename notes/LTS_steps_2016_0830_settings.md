
### (1) Copy the settings template

Within the ```miniverse``` project directory, run the following line:

```
cp miniverse/settings/lts_settings_template.py miniverse/settings/lts_settings.py
```

### (2) Manually update the settings in lts_settings.py

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
      ]```
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
