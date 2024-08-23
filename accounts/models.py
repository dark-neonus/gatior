from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.templatetags.static import static


class Account(AbstractUser):
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._-]{4,}$',
        message=_('Username can only contain letters, numbers, dots, and underscores.')
    )

    email = models.EmailField(
        _("email address"),
        unique=True,
        blank=False,
        null=False,
        help_text=_('Required. Your email addres.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
        )

    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. Your personal identificator. 20 characters or fewer. Letters, numbers, dots, hyphenses and underscores only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(
        _("first name"),
        max_length=20,
        help_text=_('Required. Your first name you want to be known by.'),
    )
    
    last_name = models.CharField(
        _("last name"),
        max_length=20,
        blank=True,
        help_text=_('Optional. Your last name you want to be known by.'),
    )

    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pictures/%Y/%m/%d/',
        blank=True,
        null=True,
        default=None,
        help_text=_('Optional. Upload a profile picture.'),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = ["email", "first_name", "password"]


    def __str__(self) -> str:
        return "@" + self.username

    def get_profile_picture_url(self):
        """
        Returns the user's profile picture if available; otherwise returns a default image.
        """
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return static('gatior/images/default-user-icon.svg')

    def get_full_name(self) -> str:
        return self.first_name + (f" {self.last_name}" if self.last_name else "")
    
NOT_ONLY_WHITESAPCE_REGEX = r'^(?!\s*$).+'

class Post(models.Model):
    user = models.ForeignKey(Account, related_name='posts', on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to='post_images/%Y/%m/%d/',
        blank=False,
        null=False,
        help_text=_('Optional. Upload image for post.'),
    )

    body_validator = RegexValidator(
        regex=NOT_ONLY_WHITESAPCE_REGEX,
        message=_('Text can\'t contain only spaces.')
    )
    body = models.CharField(
        max_length=1200,
        blank=False,
        null=False,
        validators=[body_validator],
    )

    created_at = models.DateTimeField(_("created_at"), default=timezone.now)

    def __str__(self):
        return f"Post #{self.pk} by @{self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    body_validator = RegexValidator(
        regex=NOT_ONLY_WHITESAPCE_REGEX,
        message=_('Text can\'t contain only spaces.')
    )
    body = models.CharField(
        max_length=600,
        blank=False,
        null=False,
        validators=[body_validator],
    )

    created_at = models.DateTimeField(_("created_at"), default=timezone.now)

    def __str__(self):
        return f"Comment #{self.pk} on post #{self.post.pk} by @{self.user.username}"

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    created_at = models.DateTimeField(_("created_at"), default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Like #{self.pk} on post #{self.post.pk} by @{self.user.username}"
