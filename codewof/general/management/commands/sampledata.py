"""Module for the custom Django sampledata command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import UserType
from allauth.account.models import EmailAddress
from tests.users.factories import UserFactory
from tests.research.factories import (
    StudyFactory,
    StudyGroupFactory,
)

LOG_HEADER = '\n{}\n' + ('-' * 20)


class Command(management.base.BaseCommand):
    """Required command class for the custom Django sampledata command."""

    help = "Add sample data to database."

    def handle(self, *args, **options):
        """Automatically called when the sampledata command is given."""
        if settings.DEPLOYMENT_TYPE == 'prod' and not settings.DEBUG:
            raise management.base.CommandError(
                'This command can only be executed in DEBUG mode on non-production website.'
            )

        # Clear all data
        print(LOG_HEADER.format('Wipe database'))
        management.call_command('flush', interactive=False)
        print('Database wiped.')

        management.call_command('load_user_types')
        print(LOG_HEADER.format('Create sample users'))
        User = get_user_model()
        # Create admin account
        admin = User.objects.create_superuser(
            'admin',
            'admin@codewof.co.nz',
            password=settings.SAMPLE_DATA_ADMIN_PASSWORD,
            first_name='Admin',
            last_name='Account',
            user_type=UserType.objects.get(slug='teacher')
        )
        EmailAddress.objects.create(
            user=admin,
            email=admin.email,
            primary=True,
            verified=True
        )
        print('Admin created.')

        # Create user account
        user = User.objects.create_user(
            'user',
            'user@codewof.co.nz',
            password=settings.SAMPLE_DATA_USER_PASSWORD,
            first_name='Alex',
            last_name='Doe',
            user_type=UserType.objects.get(slug='student')
        )
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True
        )
        UserFactory.create_batch(size=100)
        print('Users created.')

        # Codewof
        management.call_command('load_questions')
        print('Programming questions loaded.')

        # Research
        StudyFactory.create_batch(size=5)
        StudyGroupFactory.create_batch(size=15)
        print('Research studies loaded.')
