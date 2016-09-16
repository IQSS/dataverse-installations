from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from dv_apps.datafiles.models import FileMetadata

class FixContentTypeForm(forms.Form):
    """
    Evaluate classification parameters to be used for a new layer style
    """
    file_extension = forms.CharField()
    new_content_type = forms.CharField()


    def clean_file_extension(self):

        ext_str = self.cleaned_data.get('file_extension')

        print 'ext_str', ext_str

        if not ext_str.startswith('.'):
            raise forms.ValidationError(
                _('The file extension must start with a "." value.  Extension was: "%s"' % ext_str)
                )

        if self.has_quotes_or_whitespace(ext_str):
            raise forms.ValidationError(
                _('The file extension cannot have whitepspace, single quotes or double quotes.  Extension was: "%s"' % ext_str)
                )

        if FileMetadata.objects.filter(label__endswith=ext_str).count() == 0:
            raise forms.ValidationError(
                _('There are no files with extension: "%s"' % ext_str )
                )

        return ext_str

    def has_quotes_or_whitespace(self, some_str):

        if some_str.find('"') > -1 or some_str.find('\'') > -1:
            return True

        if len(some_str) != len(''.join(some_str.split())):
            return True

        return False


    def clean_new_content_type(self):

        new_content_type = self.cleaned_data.get('new_content_type')

        if self.has_quotes_or_whitespace(new_content_type):
            raise forms.ValidationError(
                _('The file extension cannot have whitepspace, single quotes or double quotes.  Extension was: "%s"' % new_content_type)
                )

        return new_content_type


    def get_fix_instructions(self):

        if not hasattr(self, 'cleaned_data'):
            raise Exception('To use this method, call "is_valid" and make sure its true.')

        d = dict(file_extension=self.cleaned_data['file_extension'],
                new_content_type=self.cleaned_data['new_content_type'])

        return render_to_string('metrics/maintenance/fix_content_type.md', d)
