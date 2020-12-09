# Generated by Django 3.1.4 on 2020-12-09 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0004_auto_20201209_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
