from django import forms
from django.contrib.auth.models import User

from .models import StudentProfile
class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Full Name",
            "autocomplete": "name"
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username",
            "autocomplete": "username"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Address",
            "autocomplete": "email"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
            "autocomplete": "new-password"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password",
            "autocomplete": "new-password"
        })
    )


    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            'email',
            'password'
        ]



    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match"
            )

        return cleaned_data




class StudentProfileForm(forms.ModelForm):

    class Meta:

        model = StudentProfile

        fields = [

            "profile_image",

            "phone",

            "location",

            "bio",

            "learning_goal",

        ]

        widgets = {

            "phone": forms.TextInput(attrs={
                "class":"form-control"
            }),

            "location": forms.TextInput(attrs={
                "class":"form-control"
            }),

            "bio": forms.Textarea(attrs={
                "class":"form-control",
                "rows":4
            }),

            "learning_goal": forms.TextInput(attrs={
                "class":"form-control"
            }),

        }