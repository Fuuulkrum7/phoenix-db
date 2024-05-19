## @package superuser_creation
#  This module sets up the Django environment and creates a superuser if one does not already exist.
#

## @file superuser_creation_script
#  This script initializes the Django framework settings and creates a superuser based on environment variables.
#

import os
import django
from django.contrib.auth.models import User

# Set the default settings module for the Django project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phoenixdb.settings')

# Prepare the Django environment for use in the script.
django.setup()

# Retrieve superuser credentials from environment variables.
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phoenixdb.settings')

django.setup()

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

## Checks if a superuser with the given username already exists in the database.
#  If the user does not exist, it creates a new superuser with the provided credentials.
#  Otherwise, it reports that the superuser already exists.
#
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created')  # Inform about the creation of the superuser.
else:
    print(f'Superuser {username} already exists')  # Inform if the superuser already exists.

