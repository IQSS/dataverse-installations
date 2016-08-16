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
