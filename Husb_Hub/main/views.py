from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib import messages
from .models import User, Post, ConnectionRequest, Message, CommunityPost, Comment, CommunityComment, MoodEntry
from .forms import CustomUserCreationForm, PostForm, CommentForm, CommunityCommentForm, MoodEntryForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Hush Hub, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

@login_required
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm()
    
    # Check connections for each post author to show/hide "Connect" button
    # This is a bit inefficient for many posts, but fine for MVP
    # Better to do this in the template or with a custom template tag/filter
    
    return render(request, 'main/index.html', {
        'posts': posts, 
        'comment_form': comment_form
    })

@login_required
def create_post(request):
    if request.user.role != 'patient':
        messages.warning(request, "Only patients can create posts.")
        return redirect('index')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            request.user.points += 10
            request.user.save()
            messages.success(request, "Post created successfully! (+10 points)")
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {'form': form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            request.user.points += 2
            request.user.save()
            messages.success(request, "Comment added! (+2 points)")
    return redirect('index')

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        # Optional: Award points to author?
        post.author.points += 1
        post.author.save()
        
    return redirect('index')

@login_required
def connect_from_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        messages.warning(request, "You cannot connect with yourself.")
        return redirect('index')
        
    # Check if already connected or pending
    existing = ConnectionRequest.objects.filter(
        (Q(sender=request.user) & Q(receiver=post.author)) |
        (Q(sender=post.author) & Q(receiver=request.user))
    ).exists()
    
    if existing:
        messages.info(request, "Connection request already exists or you are already connected.")
    else:
        ConnectionRequest.objects.create(sender=request.user, receiver=post.author)
        messages.success(request, "Connection request sent!")
        
    return redirect('index')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all().order_by('-created_at')
    
    # Connection logic
    connection_status = None
    if request.user != user:
        # Check if there is a request
        outgoing = ConnectionRequest.objects.filter(sender=request.user, receiver=user).first()
        incoming = ConnectionRequest.objects.filter(sender=user, receiver=request.user).first()
        
        if outgoing:
            connection_status = f"Request {outgoing.status}"
        elif incoming:
            connection_status = f"Incoming request ({incoming.status})"
            
    return render(request, 'main/profile.html', {
        'profile_user': user,
        'posts': posts,
        'connection_status': connection_status
    })

@login_required
def send_connection_request(request, username):
    receiver = get_object_or_404(User, username=username)
    if request.user != receiver:
        ConnectionRequest.objects.get_or_create(sender=request.user, receiver=receiver)
        messages.success(request, f"Connection request sent to {username}!")
    return redirect('profile', username=username)

@login_required
def manage_requests(request):
    received_requests = request.user.received_requests.filter(status='pending')
    return render(request, 'main/manage_requests.html', {'requests': received_requests})

@login_required
def accept_request(request, request_id):
    req = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
    req.status = 'accepted'
    req.save()
    
    # Award points
    request.user.points += 50
    request.user.save()
    
    # Auto-decline other requests if user is a patient
    if request.user.role == 'patient':
        other_requests = ConnectionRequest.objects.filter(
            receiver=request.user, 
            status='pending'
        ).exclude(id=req.id)
        for other_req in other_requests:
            other_req.status = 'rejected'
            other_req.save()
    
    messages.success(request, "Request accepted! (+50 points)")
    return redirect('manage_requests')

@login_required
def reject_request(request, request_id):
    req = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
    req.status = 'rejected'
    req.save()
    messages.info(request, "Request rejected.")
    return redirect('manage_requests')

@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Verify connection exists
    connection = ConnectionRequest.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user)),
        status='accepted'
    ).exists()
    
    if not connection:
        messages.error(request, "You are not connected with this user.")
        return redirect('index')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            request.user.points += 5
            request.user.save()
            return redirect('chat_room', user_id=user_id)

    messages_list = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # Anonymity logic for display
    display_name = other_user.username
    if request.user.role == 'therapist' and other_user.role == 'patient':
        display_name = "Patient"

    return render(request, 'main/chat.html', {
        'other_user': other_user,
        'messages': messages_list,
        'display_name': display_name
    })

@login_required
def community_feed(request):
    if request.user.points < 100:
        return render(request, 'main/community_locked.html')
        
    posts = CommunityPost.objects.all().order_by('-created_at')
    comment_form = CommunityCommentForm()
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            CommunityPost.objects.create(author=request.user, content=content)
            messages.success(request, "Posted to community!")
            return redirect('community_feed')
            
    return render(request, 'main/community.html', {
        'posts': posts,
        'comment_form': comment_form
    })

@login_required
def add_community_comment(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    if request.method == 'POST':
        form = CommunityCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added!")
    return redirect('community_feed')

@login_required
def toggle_community_like(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('community_feed')

def chat_placeholder(request):
    return render(request, 'main/chat_placeholder.html')

@login_required
def self_care(request):
    # Handle Mood Entry
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.save()
            messages.success(request, "Mood tracked successfully!")
            return redirect('self_care')
    else:
        form = MoodEntryForm()

    # Get mood history
    mood_history = request.user.mood_entries.all().order_by('-created_at')[:7] # Last 7 entries

    return render(request, 'main/self_care.html', {
        'form': form,
        'mood_history': mood_history
    })

def self_care_placeholder(request):
    return redirect('self_care')
