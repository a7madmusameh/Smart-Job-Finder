# Generated by Django 5.0.6 on 2024-05-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0002_dataofcv"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="filepdf",
            field=models.FileField(upload_to="testfile/file"),
        ),
    ]