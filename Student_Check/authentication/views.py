from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from authentication.models import Profile
from authentication.forms import ProfessorSignupForm, ProfessorSigninForm, StudentSignupForm
from student_discussion.models import Feedback, Professor


def welcome(request):
    """
    Displays the welcome page or redirects based on user type.
    """
    return render(request, "authentication/welcome.html")

def user_dashboard(request, user_type):
    if user_type == 'student':
        return render(request, 'student_dashboard.html', {'user_type': 'student'})
    elif user_type == 'professor':
        return render(request, 'professor_dashboard.html', {'user_type': 'professor'})
    else:
        return redirect('welcome')  # Default redirection in case of an error

def professor_signup(request):
    if request.method == 'POST':
        form = ProfessorSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.is_professor = True  # Ensure the user is marked as a professor
            user.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('professor_signin')  # Redirect to signin page
        else:
            messages.error(request, 'Error creating your account. Please check the form.')
    else:
        form = ProfessorSignupForm()

    return render(request, 'authentication/professor_signup.html', {'form': form})


def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Ensure the password is hashed
            user.is_student = True  # You may need to create this field in your model
            user.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('student_signin')  # Redirect to the student_signin page
        else:
            messages.error(request, 'Error creating your account. Please check the form.')
    else:
        form = StudentSignupForm()

    return render(request, 'authentication/student_signup.html', {'form': form})

def professor_signin(request):
    if request.method == 'POST':
        form = ProfessorSigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:  # Check if the user is a staff member
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('professor_home')  # Redirect to your discussion homepage
                else:
                    messages.error(request, "Access restricted to professors only.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = ProfessorSigninForm()

    return render(request, 'professor_login.html', {'form': form})

def signout(request):
    """
    Logs out the currently authenticated user and redirects to the home page.
    """
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('welcome')  # Redirect to the home page after logging out


def student_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If credentials are correct, log the user in
            login(request, user)
            # Redirect to chatroom home page (assuming 'chatroom_home' is the name of the URL)
            return redirect('discussion_home')
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password.")

    # Render the sign-in page if it's a GET request or failed POST
    return render(request, 'student_signin.html')


  # Import your models

@login_required
def professor_home(request):
    try:
        # Get the logged-in professor instance
        professor = Professor.objects.get(user=request.user)  # Assuming `Professor` has a OneToOneField to `User`
        feedbacks = Feedback.objects.filter(professor=professor)
    except Professor.DoesNotExist:
        # Handle case where the user is not a professor
        feedbacks = []
    return render(request, 'authentication/professor_home.html', {'feedbacks': feedbacks})

def feedback_success(request):
    return render(request, 'student_discussion/feedback_success.html')


