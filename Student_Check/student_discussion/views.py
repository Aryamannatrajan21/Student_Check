# student_discussion/views.py
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from authentication.forms import FeedbackForm, ProfessorSignupForm
from student_discussion.models import ChatRoom, ChatMessage, Feedback


@login_required
def discussion_home(request):
    return render(request, 'student_discussion/discussion_home.html')






@login_required
def create_chat_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name').strip().lower()  # Normalize the room name
        description = request.POST.get('description', '')

        # Check if a chat room with this normalized name already exists
        if ChatRoom.objects.filter(name=room_name).exists():
            error_message = 'A chat room with this name already exists. Please choose a different name.'
            return render(request, 'student_discussion/create_chat_room.html', {'error': error_message})

        try:
            # If no room exists, create a new chat room
            chatroom = ChatRoom.objects.create(name=room_name, description=description)
            return redirect('chatroom', chatroom_id=chatroom.id)

        except IntegrityError:
            error_message = 'There was a problem creating the chat room. Please try again.'
            return render(request, 'student_discussion/create_chat_room.html', {'error': error_message})

    return render(request, 'student_discussion/create_chat_room.html')


@login_required
@login_required
def give_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user  # Set the logged-in student
            feedback.save()
            return redirect('feedback_success')  # Redirect after success
    else:
        form = FeedbackForm()

    return render(request, 'student_discussion/give_feedback.html', {'form': form})

@login_required
def view_feedback(request):
    if hasattr(request.user, 'professor_profile'):
        feedbacks = Feedback.objects.filter(professor=request.user.professor_profile)
        return render(request, 'student_discussion/view_feedback.html', {'feedbacks': feedbacks})
    return render(request, 'student_discussion/access_denied.html')
@login_required
def chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    messages = ChatMessage.objects.filter(chatroom=chatroom).order_by('timestamp')

    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            ChatMessage.objects.create(chatroom=chatroom, sender=request.user, content=message_content)
            return redirect('chatroom', chatroom_id=chatroom.id)

    context = {
        'chatroom': chatroom,
        'messages': messages
    }

    return render(request, 'student_discussion/chatroom.html', context)


@login_required
def send_message(request, chatroom_id):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        file = request.FILES.get('file')  # Get the uploaded file

        # Create and save the message
        message = ChatMessage(
            chatroom_id=chatroom_id,
            sender=request.user,
            content=message_content,
            file=file if file else None
        )
        message.save()

        return redirect('chatroom', chatroom_id=chatroom_id)

def join_chatroom(request):
    """
    View to handle joining an existing chatroom by name.
    """
    if request.method == 'POST':
        chatroom_name = request.POST.get('chatroom_name')

        try:
            # Check if the chatroom exists by name
            chatroom = ChatRoom.objects.get(name=chatroom_name)

            # If found, redirect to that chatroom
            return redirect('chatroom', chatroom_id=chatroom.id)

        except ChatRoom.DoesNotExist:
            # If chatroom doesn't exist, show an error message on the discussion home page
            return render(request, 'student_discussion/discussion_home.html', {
                'error': 'Chatroom does not exist. Please enter a valid chatroom name.'
            })

    return redirect('discussion_home')

def professor_signup(request):
    if request.method == 'POST':
        form = ProfessorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('professor_login')
    else:
        form = ProfessorSignupForm()
    return render(request, 'student_discussion/professor_signup.html', {'form': form})

def professor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('professor_dashboard')  # Redirect to the professor dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'student_discussion/professor_dashboard.html', {'form': form})


# student_discussion/views.py
@login_required
def professor_dashboard(request):
    if hasattr(request.user, 'professor_profile'):
        feedbacks = request.user.professor_profile.feedbacks.all()
        return render(request, 'student_discussion/professor_dashboard.html', {'feedbacks': feedbacks})
    return redirect('professor_login')
