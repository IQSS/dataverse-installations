from django.db import models
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible

class AuthenticatedUser(models.Model):
    useridentifier = models.CharField(unique=True, max_length=255)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    modificationtime = models.DateTimeField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    superuser = models.NullBooleanField()

    def is_superuser(self):
        if not self.superuser:
            return False

        if self.superuser is True:
            return True

        return False


    def __str__(self):
        if self.lastname and self.firstname:
            return '%s (%s, %s)' % (self.useridentifier, self.lastname, self.firstname)
        elif self.lastname:
            return '%s (%s)' % (self.useridentifier, self.lastname)
        else:
            return self.useridentifier

    class Meta:
        ordering = ('useridentifier',)
        managed = False
        db_table = 'authenticateduser'


class ApiToken(models.Model):
    authenticateduser = models.ForeignKey('Authenticateduser')
    tokenstring = models.CharField(unique=True, max_length=255)
    disabled = models.BooleanField()
    expiretime = models.DateTimeField()
    createtime = models.DateTimeField()
    authenticateduser = models.ForeignKey('Authenticateduser')

    def __str__(self):
        return '%s - %s' % (self.authenticateduser, self.tokenstring)


    def is_expired(self):
        now = datetime.now()
        if now > self.expiretime:
            #self.disabled = True
            #self.save()
            return True
        return False

    class Meta:
        ordering = ('-expiretime', 'authenticateduser')
        managed = False
        db_table = 'apitoken'


@python_2_unicode_compatible
class BuiltInUser(models.Model):
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    encryptedpassword = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    passwordencryptionversion = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return '%s' % self.username

    class Meta:
        managed = False
        db_table = 'builtinuser'
