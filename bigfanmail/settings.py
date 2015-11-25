# Django settings for bigfanmail project.
import os

DEBUG = False
TEMPLATE_DEBUG = False

AUTH_USER_MODEL = 'customers.BFCustomer'
ADMINS = (
     ('Andy Guschwan', 'aguschwan@gmail.com'),
     ('Bob Gillespie', 'bob@theg.ws'),
)

MANAGERS = ADMINS

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_live_CGgHX8jlzetasWESfzPWtZOo")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_live_exQ08l4s934bOLw7rg4b9dDt")
#STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_live_jRYdKNcCJVkkp7Y2Q8gLOppt")

PAYMENTS_PLANS = {
        "trialstandard": {
           "stripe_plan_id": "trialstandard",
           "name": "Big Fan Mail Standard ($15.00/year)",
           "description": "The annual subscription plan to BigFanMail",
           "price": 15.00,
           "currency": "usd",
           "interval": "year"
        },
        "trialpremium": {
           "stripe_plan_id": "trialpremium",
           "name": "Big Fan Mail Standard ($30.00/year)",
           "description": "The annual subscription plan to BigFanMail",
           "price": 30.00,
           "currency": "usd",
           "interval": "year"
        },
        "ultra-premium": {
           "stripe_plan_id": "ultra-premium",
           "name": "Big Fan Mail Ultra-Premium ($79.99/year)",
           "description": "The annual subscription plan to BigFanMail",
           "price": 79.99,
           "currency": "usd",
           "interval": "year"
        }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bigfanprddb',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'gooseswan',
        'PASSWORD': 'cubs2010',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.bigfanmail.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/gooseswan/webapps/staticstuff/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/home/gooseswan/webapps/bfmdjango/static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0a!cf2&spitz^_@^8smzqvx^^=@4&l6knq-o%vy-2_!tso9yz&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bigfanmail.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bigfanmail.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/home/gooseswan/webapps/bfmdjango/bigfantemplates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'registration',
    'bigfanmail.customers',
    'bigfanmail.domains',
    'bigfanmail.products',
    'django_localflavor_us',
    'payments',
    'django_forms_bootstrap',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # I always add this handler to facilitate separating loggings
        'log_file':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            #'filename': os.path.join('/opt/local', 'logs/django.log'),
            'filename': '/home/gooseswan/webapps/bfmdjango/django.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'registration': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'bigfanmail': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    'root': {
        'handlers': ['log_file'],
        'level': 'DEBUG'
    },
}
ACCOUNT_ACTIVATION_DAYS = 7
TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.core.context_processors.request",
"django.contrib.messages.context_processors.messages")
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'bigfanmail'
EMAIL_HOST_PASSWORD = 'Sandberg23!'
DEFAULT_FROM_EMAIL = 'support@bigfanmail.com'
SERVER_EMAIL = 'support@bigfanmail.com'
