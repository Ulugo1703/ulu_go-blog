# Generated by Django 4.2.5 on 2024-04-08 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0006_like_dislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='dislike',
            name='comment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='blog_app.comment'),
        ),
        migrations.AddField(
            model_name='like',
            name='comment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blog_app.comment'),
        ),
    ]
