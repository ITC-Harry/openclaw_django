from django import forms
from .models import Issue, Comment


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['summary', 'description', 'issue_type', 'priority',
                  'status', 'assignee', 'labels']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'labels': forms.TextInput(attrs={'placeholder': 'bug, frontend, urgent'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': '新增評論...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
