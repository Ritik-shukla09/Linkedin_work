from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile
from django import forms
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_image",
            "headline",
            "bio",
            "location",
            "company",
            "college",
            "skills",   
        ]

        widgets = {
            "headline": forms.TextInput(attrs={
                "placeholder": "Your professional headline"
            }),
            "bio": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Tell something about yourself"
            }),
            "location": forms.TextInput(attrs={
                "placeholder": "City, Country"
            }),
            "company": forms.TextInput(attrs={
                "placeholder": "Current company"
            }),
            "college": forms.TextInput(attrs={
                "placeholder": "College / University"
            }),
            "skills": forms.TextInput(attrs={   
                "placeholder": "Python, Django, React, SQL"
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


from .models import Experience, Project


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["company", "role", "start_date", "end_date", "description"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "tech_stack", "project_link"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


from .models import Education

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "field_of_study",
            "start_year",
            "end_year",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
