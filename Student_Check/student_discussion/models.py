from django.db import models
from django.contrib.auth.models import User




class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor_profile")
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Feedback(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.student} to {self.professor}"



class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.chatroom}"



