The github repository is here: https://github.com/iqss/miniverse

The application's python libraries can be installed using pip and virtualenv. It's python 2.711 and Django 1.9

One of the questions is: which web server you plan to use and how that relates to production settings such as passwords (e.g. databases, etc). e.g. If it's apache, I'll need to make a specific settings file, if it's gunicorn/nginx, these settings may be saved as environment variables, etc.

Main steps:

  - (A) Let me know what type of server you will be using so I can start an appropriate settings file
  - (B) Go through steps 1 through 6 below
  - (C) Let me know non-passwords values from (B). I can finish the settings file based on (A) and (B)
  - (D) Run through the install with the settings file. See #8 below (I'll write that out later today but with 1 or 2 exceptions it's similar to the README on the github page)

Set-up:

### (1) https cert

Certificate for the name "services.dataverse.harvard.edu" (This had been created about 2 years ago and wen unused)

### (2) Dataverse database permissions. (scope of the original ticket)

Permissions to read** the existing Dataverse postgres database.
- username: "miniverse_user"
- password: BD (please set at your discretion)
** e.g., "Select" on all tables in the Dataverse database ("dvndb")

### (3) Second database.

Create a new postgres database and credentials to give the app full table create/write access. This stores the Django/Miniverse specific information.
- database name: "miniverse_default"
- username: "miniverse_user"
- password: TBD (please set at your discretion)

### (4) Email.

B/c this was on Heroku, we were using gmail to send 404/500 messages to admins via port 587.
  - Since we are on Harvard's network, what do you suggest for an email server.
  - Is there a fasmail server that we can use? Do we need credentials? This is only for admin messages: 404/500

### (5) Static files directory.

Set up a directory for serving statics files--images, css, javascript, etc. Note this also includes several HTML files.
  - The static files are in Github andhttps://docs.djangoproject.com/en/1.9/ref/settings/#media-root after set-up Django copies them to the "static files directory" specified in the settings file.
  - Reference: https://docs.djangoproject.com/en/1.9/howto/static-files/#deployment

### (6) Media files directory

An administrative user may upload files--such as logo files for a map. (This probably won't be often). We need a directory separate from (5) where the web server can write files as well as serve the to the public. As part of set-up we will also need to copy files from (miniverse admin)/media/logos to this directory

  - Reference: https://docs.djangoproject.com/en/1.9/ref/settings/#media-root

### (7) Django settings file

Once all of the above are decided, I can make a Django specific settings file--where the values are either in the file or it reads them from environment variables

  - Note: These are the current heroku dev settings:
    - https://github.com/IQSS/miniverse/blob/master/miniverse/settings/heroku_dev.py

  - Several of which overwrite the "base" settings:   - https://github.com/IQSS/miniverse/blob/master/miniverse/settings/base.py

### (8) Once all the settings are in place, let's talk. Basically, I think you can follow these steps:

  - https://github.com/IQSS/miniverse#step-4-test-your-settings-and-run-the-dev-server

Also, the "logos" directory in "miniverse/logos/*" will need to be copied to (6)

**Except**: Don't run the local server
