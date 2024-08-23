# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Account, Post, Comment, Like

class PostsInline(admin.TabularInline):
    model = Post
    extra = 1
    classes = ["collapse",]

class AccountAdmin(UserAdmin):
    model = Account

    list_display = ["username", "email", "first_name", "last_name", "pk"]
    list_filter = ["date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]

    # Override UserAdmin fieldsets and add collapse class to specific sections
    fieldsets = (
        ("Login info", {
            'fields': ('username', 'email'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'profile_picture'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups'),
            'classes': ('collapse',)  # Make this section collapsible
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)  # Make this section collapsible
        }),
    )

    add_fieldsets = (
        ("Login info", {
            'fields': ['username', 'email', 'password1', 'password2'],
        }),
        ('Personal info', {
            'fields': ['first_name', 'last_name', 'profile_picture'],
        }),
    )

    inlines = [PostsInline]
class LikeInline(admin.TabularInline):
    model = Like
    extra = 2
    classes = ["collapse",]

class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 1
    classes = ["collapse",]

class PostAdmin(admin.ModelAdmin):
    model = Post
    fieldsets = [
        (None, {"fields" : ["user", "image", "body", "created_at"]}),
    ]
    inlines = [LikeInline, CommentsInline]
    list_display = ["__str__", "created_at"]

    list_filter = ["created_at"]
    search_fields = ["body"]

    

    
admin.site.register(Account, AccountAdmin)
admin.site.register(Post, PostAdmin)
