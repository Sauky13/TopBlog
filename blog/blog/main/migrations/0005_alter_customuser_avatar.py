# Generated by Django 5.0 on 2023-12-11 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='images/avatars/default.jpg', null=True, upload_to='images/avatars/'),
        ),
    ]