# Generated by Django 5.0.4 on 2025-03-17 14:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitypost',
            name='author',
        ),
        migrations.RemoveField(
            model_name='communitypost',
            name='likes',
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='address',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='website',
        ),
        migrations.AddField(
            model_name='hotel',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='CommunityPost',
        ),
    ]
