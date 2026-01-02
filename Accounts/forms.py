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
from django import forms
from .models import Profile

from django import forms
from .models import Profile

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
            "skills",   # ✅ ADD THIS
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
            "skills": forms.TextInput(attrs={   # ✅ ADD THIS
                "placeholder": "Python, Django, React, SQL"
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })