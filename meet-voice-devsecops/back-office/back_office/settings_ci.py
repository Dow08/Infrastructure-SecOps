"""
Settings CI/CD — GitHub Actions
================================
Utilisé exclusivement en pipeline CI (DJANGO_SETTINGS_MODULE=back_office.settings_ci).
- Aucun tunnel SSH (pas d'accès aux serveurs depuis GitHub Actions)
- Base de données SQLite en mémoire (rapide, sans dépendances externes)
- Secrets factices sûrs (non utilisés en production)
- Tous les INSTALLED_APPS et MIDDLEWARE identiques à production
"""

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Sécurité ─────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='ci-only-insecure-key-not-for-production-42x!')
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ── Applications ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'content',
    'compte',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'back_office.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'back_office.wsgi.application'

# ── Bases de données — SQLite en mémoire (CI uniquement) ─────────────────────
# Aucune connexion externe nécessaire — les tests s'exécutent sans réseau.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {'NAME': ':memory:'},
    },
    'articles': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {'NAME': ':memory:'},
    },
}

# ── MongoDB — désactivé en CI (pas de connexion) ──────────────────────────────
MONGO_DATABASES = {}

# ── Cache — mémoire locale (pas de Redis en CI) ───────────────────────────────
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 300,
        'OPTIONS': {'MAX_ENTRIES': 500},
    }
}

# ── Routeur de base de données ────────────────────────────────────────────────
DATABASE_ROUTERS = ['content.db_router.ArticleRouter']

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# ── Fichiers statiques ────────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Auth ──────────────────────────────────────────────────────────────────────
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── APIs externes — désactivées en CI ────────────────────────────────────────
MOLLIE_API_KEY = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
SMTP_HOST = ''
SMTP_USER = ''
SMTP_PASSWORD = ''
LINKEDIN_CLIENT_ID = ''
LINKEDIN_CLIENT_SECRET = ''
LINKEDIN_ORG_ID = ''
LINKEDIN_REDIRECT_URI = 'http://127.0.0.1:8000/social-analytics/linkedin/callback/'
FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''
LATE_API_KEY = ''
REDIS_URL = ''
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
