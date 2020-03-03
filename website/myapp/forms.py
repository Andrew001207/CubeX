from django import forms


class CubeIdForm(forms.Form):
    cube_id = forms.IntegerField(label='cube_id')

class TaskForm(forms.Form):
    task_name = forms.CharField(label='task_name')
    task_group = forms.CharField(label='task_group')
    cube_id = forms.IntegerField(label='cube_id')
