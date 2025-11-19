from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Comment, CommunityComment, MoodEntry

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'is_anonymous']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...', 'class': 'form-control'}),
        }

class CommunityCommentForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...', 'class': 'form-control'}),
        }

class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'note']
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'How are you feeling today?'}),
        }
