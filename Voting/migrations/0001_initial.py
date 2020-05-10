# Generated by Django 3.0.5 on 2020-05-10 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteSU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('vote_for', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vote_for', to=settings.AUTH_USER_MODEL)),
                ('voters', models.ManyToManyField(related_name='voters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pCount', models.IntegerField(default=0)),
                ('wCount', models.IntegerField(default=0)),
                ('kickCount', models.IntegerField(default=0)),
                ('voterName', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Groups.GroupMember')),
            ],
        ),
    ]
