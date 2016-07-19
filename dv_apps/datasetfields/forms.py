from django import forms
from django.forms.widgets import TextInput


class ControlledVocabularyInlineForm(forms.ModelForm):
    """TargetedESCloneExpansionForm.  Used to size the text input boxes"""

    class Meta:
        widgets = { 'strvalue': forms.Textarea(attrs={'rows': 1, 'cols':35})}
