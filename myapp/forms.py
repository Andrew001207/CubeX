from django import forms

class CubeIdForm(forms.Form):
    cube_id = forms.IntegerField (label='cube_id')