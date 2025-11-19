from django.contrib import admin
from .models import User, Post, ConnectionRequest, Comment, CommunityPost, CommunityComment, MoodEntry, Message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'points', 'current_badge', 'is_staff']
    list_filter = ['role', 'is_staff']
    search_fields = ['username', 'email']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'is_anonymous', 'created_at', 'like_count']
    list_filter = ['is_anonymous', 'created_at']
    search_fields = ['content', 'author__username']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'created_at', 'like_count']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'

@admin.register(CommunityComment)
class CommunityCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood', 'created_at']
    list_filter = ['mood', 'created_at']
    search_fields = ['user__username', 'note']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_preview', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__username', 'receiver__username', 'content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username']
