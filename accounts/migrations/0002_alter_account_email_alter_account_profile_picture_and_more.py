# Generated by Django 5.0.7 on 2024-08-03 16:53

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="email",
            field=models.EmailField(
                error_messages={"unique": "A user with that email already exists."},
                help_text="Required. Your email addres.",
                max_length=254,
                unique=True,
                verbose_name="email address",
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default=None,
                help_text="Optional. Upload a profile picture.",
                null=True,
                upload_to="profile_pictures/%Y/%m/%d/",
                verbose_name="profile picture",
            ),
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        help_text="Optional. Upload image for post.",
                        null=True,
                        upload_to="post_images/%Y/%m/%d/",
                    ),
                ),
                (
                    "body",
                    models.CharField(
                        max_length=1200,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Text can't contain only spaces.",
                                regex="^(?!\\s*$)[a-zA-Z0-9._-]+$",
                            )
                        ],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "body",
                    models.CharField(
                        max_length=600,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Text can't contain only spaces.",
                                regex="^(?!\\s*$)[a-zA-Z0-9._-]+$",
                            )
                        ],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="accounts.post",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="accounts.post",
                    ),
                ),
            ],
            options={
                "unique_together": {("post", "user")},
            },
        ),
    ]
