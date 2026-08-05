import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Define your default superuser credentials
USERNAME = os.environ.get('SUPERUSER_USERNAME', 'admin')
EMAIL = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'admin1234')

if not User.objects.filter(username=USERNAME).exists():
    print(f"Creating superuser '{USERNAME}'...")
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print("Superuser created successfully!")
else:
    print(f"Superuser '{USERNAME}' already exists.")
