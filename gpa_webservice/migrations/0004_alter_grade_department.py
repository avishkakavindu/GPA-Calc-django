# Generated by Django 3.2.13 on 2022-10-11 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gpa_webservice', '0003_auto_20221011_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gpa_webservice.department'),
        ),
    ]