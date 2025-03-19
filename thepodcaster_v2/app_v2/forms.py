from django import forms
from .models import *

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'description', 'cover', 'keywords', 'copyright', 'language']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label
            


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['show','title', 'description', 'duration', 'audio']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label
            

           

