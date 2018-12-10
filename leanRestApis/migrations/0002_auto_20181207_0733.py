# Generated by Django 2.1.3 on 2018-12-07 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leanRestApis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leanRestApis.Activities')),
                ('parent_project_activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leanRestApis.ProjectActivity')),
            ],
        ),
        migrations.DeleteModel(
            name='ProjectActivitie',
        ),
    ]
