# Generated by Django 3.2.5 on 2021-12-13 12:24

import clubs.user_types
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.EmailField(default='', max_length=254, unique=True)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('bio', models.CharField(blank=True, default='', max_length=520)),
                ('chess_experience', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('personal_statement', models.CharField(default='', max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('location', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(1, 'CLUB_OWNER'), (2, 'OFFICER'), (3, 'MEMBER'), (4, 'APPLICANT')], default=clubs.user_types.UserTypes['APPLICANT'], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('club_membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club')),
                ('current_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='member',
            constraint=models.UniqueConstraint(condition=models.Q(('user_type', clubs.user_types.UserTypes['CLUB_OWNER'])), fields=('club_membership',), name="there can't exist more than one club owner"),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('current_user', 'club_membership')},
        ),
    ]
