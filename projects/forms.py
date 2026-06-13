from django import forms
from .models import Project, ProjectMember


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'key', 'description', 'project_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['user', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
