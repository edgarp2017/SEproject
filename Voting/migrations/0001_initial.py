# Generated by Django 3.0.4 on 2020-05-08 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteSU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('vote_for', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Users.AcceptedUser')),
            ],
        ),
    ]
