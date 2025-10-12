from django.urls import path
from .views import dashboard, register, add_affirmation, add_emergency_contact

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('add-affirmation/', add_affirmation, name='add_affirmation'),
    path('add-contact/', add_emergency_contact, name='add_contact'),
]