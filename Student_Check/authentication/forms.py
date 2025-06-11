# student_discussion/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from student_discussion.models import Feedback, Professor,  ChatMessage


class ProfessorSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")




class ProfessorSigninForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")



class StudentSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class FeedbackForm(forms.ModelForm):
    professor = forms.ModelChoiceField(
        queryset=Professor.objects.all(),  # Show all registered professors
        empty_label="Select a professor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Feedback
        fields = ['professor', 'content']




# If you have a custom Student model, use that instead
# from .models import Student  # Uncomment this if using a custom model

class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Email field
    first_name = forms.CharField(max_length=30, required=True)  # First name
    last_name = forms.CharField(max_length=30, required=True)  # Last name

    class Meta:
        model = User  # Use the User model from Django's authentication
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2']  # These are the fields that will be included in the form

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Check if email is already in use
            raise ValidationError("Email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # You can add extra logic here if needed, e.g., assigning `is_student` flag
        user.is_active = True  # Ensure user is active upon creation
        if commit:
            user.save()  # Save the user to the database
        return user

class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content', 'file']