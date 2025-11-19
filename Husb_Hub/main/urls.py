from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('connect/<str:username>/', views.send_connection_request, name='send_connection_request'),
    path('requests/', views.manage_requests, name='manage_requests'),
    path('requests/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('requests/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('chat/', views.chat_placeholder, name='chat'),
    path('chat/<int:user_id>/', views.chat_room, name='chat_room'),
    path('community/', views.community_feed, name='community_feed'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/connect/', views.connect_from_post, name='connect_from_post'),
    path('community/comment/<int:post_id>/', views.add_community_comment, name='add_community_comment'),
    path('community/like/<int:post_id>/', views.toggle_community_like, name='toggle_community_like'),
    path('self-care/', views.self_care, name='self_care'),
]
