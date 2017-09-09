# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-09 00:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('question1', models.CharField(max_length=255)),
                ('answer1', models.CharField(max_length=255)),
                ('question2', models.CharField(max_length=255)),
                ('answer2', models.CharField(max_length=255)),
                ('image', models.FileField(null=True, upload_to='business_picture')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('deal_type', models.CharField(max_length=255)),
                ('contact_email', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=255)),
                ('fine_print', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('start_date', models.CharField(max_length=255)),
                ('end_date', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='APPNAME.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventname', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=55)),
                ('details', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meetup_Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetup_bookmarks', to='APPNAME.Business')),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetup_bookmarks', to='APPNAME.Meetup')),
            ],
        ),
        migrations.CreateModel(
            name='Meetup_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetup_comments', to='APPNAME.Meetup')),
            ],
        ),
        migrations.CreateModel(
            name='Meetup_Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetup_likes', to='APPNAME.Business')),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetup_likes', to='APPNAME.Meetup')),
            ],
        ),
        migrations.CreateModel(
            name='Messageboard_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_comments', to='APPNAME.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Messageboard_Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('image', models.FileField(blank=True, null=True, upload_to='messageboard_message')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Messageboard_Message_Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_message_bookmarks', to='APPNAME.Business')),
                ('messageboard_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_message_bookmarks', to='APPNAME.Messageboard_Message')),
            ],
        ),
        migrations.CreateModel(
            name='Messageboard_Message_Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_message_likes', to='APPNAME.Business')),
                ('messageboard_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_message_likes', to='APPNAME.Messageboard_Message')),
            ],
        ),
        migrations.CreateModel(
            name='Messageboard_Message_View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('messageboard_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_message_views', to='APPNAME.Messageboard_Message')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('question1', models.CharField(max_length=255)),
                ('answer1', models.CharField(max_length=255)),
                ('question2', models.CharField(max_length=255)),
                ('answer2', models.CharField(max_length=255)),
                ('image', models.FileField(null=True, upload_to='profile_picture')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='messageboard_message_like',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_message_likes', to='APPNAME.User'),
        ),
        migrations.AddField(
            model_name='messageboard_message_bookmark',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_message_bookmarks', to='APPNAME.User'),
        ),
        migrations.AddField(
            model_name='messageboard_message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_messages', to='APPNAME.User'),
        ),
        migrations.AddField(
            model_name='messageboard_comment',
            name='messageboard_message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_comments', to='APPNAME.Messageboard_Message'),
        ),
        migrations.AddField(
            model_name='messageboard_comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messageboard_comments', to='APPNAME.User'),
        ),
        migrations.AddField(
            model_name='meetup_like',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetup_likes', to='APPNAME.User'),
        ),
        migrations.AddField(
            model_name='meetup_comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APPNAME.User'),
        ),
        migrations.AddField(
            model_name='meetup_bookmark',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetup_bookmarks', to='APPNAME.User'),
        ),
        migrations.AddField(
            model_name='meetup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetups', to='APPNAME.User'),
        ),
    ]
