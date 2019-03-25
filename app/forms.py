from django import forms
from . import models

class PetitionForm(forms.ModelForm):
    class Meta:
        model = models.Petition

class SignatureForm(forms.ModelForm):
    class Meta:
        model = models.Signature
