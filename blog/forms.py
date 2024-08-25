# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Comment, Post, Account  
    
class CreatePostForm(forms.Form):
    image = forms.ImageField(required=True)
    body = forms.CharField(
        max_length=Post._meta.get_field("body").max_length,
        widget=forms.Textarea(attrs={'rows': 8, 'cols': 40}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        post = Post()
        post.body = self.cleaned_data["body"]
        post.user = self.user

        if self.cleaned_data["image"]:
            post.image = self.cleaned_data["image"]

        if commit:
            post.save()
        return post



class CreateCommentForm(forms.Form):
    body = forms.CharField(
        max_length=Comment._meta.get_field("body").max_length,
        widget=forms.Textarea(attrs={'rows': 8, 'cols': 40}),
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment

    def save(self, commit=True):
        comment = Comment()
        comment.body = self.cleaned_data["body"]
        comment.user = self.user
        comment.post = self.post

        # user.first_name = self.cleaned_data["first_name"]
        # user.last_name = self.cleaned_data["last_name"]
        # user.email = self.cleaned_data["email"]
        # user.username = self.cleaned_data["username"]
        # user.password = self.cleaned_data["password"]
        if commit:
            comment.save()

        return comment
    
class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["profile_picture", "first_name", "last_name"]


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        account = self.user

        print(self.cleaned_data)

        if len(self.cleaned_data["first_name"]) > 0: 
            account.first_name = self.cleaned_data["first_name"]

        account.last_name = self.cleaned_data["last_name"]

        if self.cleaned_data["profile_picture"]:
            account.profile_picture = self.cleaned_data["profile_picture"]

        if commit:
            account.save()
        return account
    
    