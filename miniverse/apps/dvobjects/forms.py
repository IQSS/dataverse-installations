from django import forms

class FilterForm(forms.Form):
    DTYPE_OPTIONS = (
                ("Dataverse", "Dataverse"),
                ("Dataset", "Dataset"),
                ("DataFile", "DataFile"),
                )
    dtype = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=DTYPE_OPTIONS)