from django import forms


class PostUrlForm(forms.Form):
    url = forms.CharField(required=True)
