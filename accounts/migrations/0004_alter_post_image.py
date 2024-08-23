# Generated by Django 5.0.7 on 2024-08-13 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_comment_body_alter_comment_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                help_text="Optional. Upload image for post.",
                upload_to="post_images/%Y/%m/%d/",
            ),
        ),
    ]
