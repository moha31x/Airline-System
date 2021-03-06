"""This script performs migrations for the updated models."""
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators as dcav
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    """class to make migrations."""

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'password', models.CharField(
                        max_length=128, verbose_name='password'
                    )
                ),
                (
                    'last_login', models.DateTimeField(
                        blank=True, null=True, verbose_name='last login'
                    )
                ),
                (
                    'is_superuser', models.BooleanField(
                        default=False, verbose_name='superuser status',
                        help_text='Designates that this user has all\
                            permissions without explicitly assigning them.'
                    )
                ),
                (
                    'username', models.CharField(
                        error_messages={
                            'unique': 'A user with that username already\
                                exists.'
                        }, max_length=150, unique=True,
                        verbose_name='username', validators=[
                            dcav.UnicodeUsernameValidator()
                        ],
                        help_text='Required. 150 characters or fewer.\
                            Letters, digits and @/./+/-/_ only.'
                    )
                ),
                (
                    'first_name', models.CharField(
                        blank=True, max_length=30, verbose_name='first name'
                    )
                ),
                (
                    'last_name', models.CharField(
                        blank=True, max_length=150, verbose_name='last name'
                    )
                ),
                (
                    'email', models.EmailField(
                        blank=True, max_length=254,
                        verbose_name='email address'
                    )
                ),
                (
                    'is_staff', models.BooleanField(
                        default=False, verbose_name='staff status',
                        help_text='Designates whether the user can log into\
                            this admin site.'
                    )
                ),
                (
                    'is_active', models.BooleanField(
                        default=True, verbose_name='active',
                        help_text='Designates whether this user should be\
                            treated as active. Unselect this instead of\
                            deleting accounts.'
                    )
                ),
                (
                    'date_joined', models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='date joined'
                    )
                ),
                (
                    'user_type', models.PositiveSmallIntegerField(
                        choices=[(1, 'flightstaff'), (2, 'admin')], default=1
                    )
                ),
                (
                    'groups', models.ManyToManyField(
                        blank=True, related_name='user_set',
                        related_query_name='user', to='auth.Group',
                        verbose_name='groups'
                    )
                ),
                (
                    'user_permissions', models.ManyToManyField(
                        blank=True, related_name='user_set',
                        related_query_name='user', to='auth.Permission',
                        verbose_name='user permissions',
                        help_text='Specific permissions for this user.'
                    )
                ),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                (
                    'flight_no', models.IntegerField(
                        default=1007, primary_key=True, serialize=False
                    )
                ),
                ('airline_name', models.CharField(max_length=50)),
                ('no_of_seats', models.IntegerField(default=0)),
                ('source', models.CharField(max_length=50)),
                ('source_code', models.CharField(max_length=3)),
                ('destination', models.CharField(max_length=50)),
                ('destination_code', models.CharField(max_length=3)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('cost', models.IntegerField(default=500)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                (
                    'id', models.IntegerField(
                        primary_key=True, serialize=False
                    )
                ),
                (
                    'flight_no', models.ManyToManyField(
                        blank=True, related_name='staffs', to='flights.Flight'
                    )
                ),
                (
                    'user', models.OneToOneField(
                        default=1, to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('pnr', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('ppno', models.CharField(max_length=50)),
                ('dob', models.DateField(default=0.0005025125628140704)),
                ('nationality', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=1)),
                ('checked_in_status', models.BooleanField(default=0)),
                (
                    'booked_by', models.ForeignKey(
                        default='moha', to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE
                    )
                ),
                (
                    'flight_no', models.ForeignKey(
                        default=1007, related_name='passengers',
                        to='flights.Flight',
                        on_delete=django.db.models.deletion.CASCADE
                    )
                ),
            ],
        ),
    ]
