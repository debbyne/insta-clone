# Generated by Django 4.0.3 on 2022-04-03 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='time_created',
            new_name='time_posted',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='followed',
            new_name='total_followed',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='total_followers',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='time_created',
            new_name='time_posted',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='profile_picture',
            new_name='profile_photo',
        ),
        migrations.AddField(
            model_name='profile',
            name='followers_ig',
            field=models.ManyToManyField(blank=True, related_name='followers_profile', to='insta.profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='following_ig',
            field=models.ManyToManyField(blank=True, related_name='following_profile', to='insta.profile'),
        ),
    ]
