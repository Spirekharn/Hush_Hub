from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import DailyAffirmationForm, EmergencyContactForm
from .models import DailyAffirmationLog

@login_required
def dashboard(request):
    badges = []
    affirmations = DailyAffirmationLog.objects.filter(user=request.user)
    contacts = EmergencyContact.objects.filter(user=request.user)
    context = {
        'badges': badges,
        'affirmations': affirmations,
        'contacts': contacts,
    }
    return render(request, 'accounts/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def add_affirmation(request):
    if request.method == 'POST':
        form = DailyAffirmationForm(request.POST)
        if form.is_valid():
            affirmation = form.save()
            DailyAffirmationLog.objects.create(user=request.user, affirmation=affirmation)
            return redirect('dashboard')
    else:
        form = DailyAffirmationForm()
    return render(request, 'accounts/add_affirmation.html', {'form': form})

@login_required
def add_emergency_contact(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('dashboard')
    else:
        form = EmergencyContactForm()
    return render(request, 'accounts/add_emergency_contact.html', {'form': form})