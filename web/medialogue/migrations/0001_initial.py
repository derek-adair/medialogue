# Generated by Django 3.2.12 on 2022-07-17 18:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import medialogue.models
import sortedm2m.fields
import video_encoding.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateTimeField(blank=True, help_text='Date image was taken; is obtained from the image EXIF data.', null=True, verbose_name='date taken')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='title')),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', max_length=250, unique=True, verbose_name='slug')),
                ('caption', models.TextField(blank=True, verbose_name='caption')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
                ('is_public', models.BooleanField(default=True, help_text='Public photographs will be displayed in the default views.', verbose_name='is public')),
                ('sites', models.ManyToManyField(blank=True, to='sites.Site', verbose_name='sites')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('media_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medialogue.media')),
                ('src', models.ImageField(upload_to=medialogue.models.get_storage_path, verbose_name='src')),
            ],
            bases=('medialogue.media',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('media_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medialogue.media')),
                ('thumbnail', models.ImageField(blank=True, upload_to='')),
                ('width', models.PositiveIntegerField(editable=False, null=True)),
                ('height', models.PositiveIntegerField(editable=False, null=True)),
                ('duration', models.FloatField(editable=False, null=True)),
                ('src', video_encoding.fields.VideoField(height_field='height', upload_to='', width_field='width')),
            ],
            bases=('medialogue.media',),
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='title')),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', max_length=250, unique=True, verbose_name='title slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('is_public', models.BooleanField(default=True, help_text='Public albums will be displayed in the default views.', verbose_name='is public')),
                ('media', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='albums', to='medialogue.Media', verbose_name='media')),
                ('sites', models.ManyToManyField(blank=True, to='sites.Site', verbose_name='sites')),
            ],
            options={
                'verbose_name': 'Album',
                'verbose_name_plural': 'Albums',
                'ordering': ['-date_added'],
                'get_latest_by': 'date_added',
            },
        ),
    ]
