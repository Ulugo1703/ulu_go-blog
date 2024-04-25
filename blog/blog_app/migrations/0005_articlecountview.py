# Generated by Django 4.2.5 on 2024-04-08 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_commentreply'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCountView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_app.article')),
            ],
        ),
    ]