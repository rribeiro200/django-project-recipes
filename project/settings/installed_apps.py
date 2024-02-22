# Application definition
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # CORS Headers
    'corsheaders',
    # Django rest framework
    'rest_framework',
    'rest_framework_simplejwt',
    # Meus apps
    'tag',
    'recipes',
    'authors',
]