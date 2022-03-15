from .base import *  # noqa
# from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="orClayuhAOwZg4nULNMYScgNQzPkhyF2pmG48ueUFsp20YCePUmSYzoZz8CFlqDh",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
ALLOWED_HOSTS = ["*"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER", default="no") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': env("ENGINE", default="django.db.backends.oracle"),
        'NAME': (
                    '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.32.254.32)(PORT=1521))'
                    '(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=BBTSTDB1)))'
                ),
        'USER':  env("USER", default="ereturns_stg"),
        'PASSWORD': env("PASSWORD", default="Epassw0rdStg"),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': env.int("CONN_MAX_AGE", default=60)  # noqa F405
    },
    'rit_mngt': {
        'ENGINE': env("ENGINE", default="django.db.backends.oracle"),
        'NAME': (
                    '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.32.254.32)(PORT=1521))'
                    '(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=BBTSTDB1)))'
                ),
        'USER':  env("RIT_USER", default="rit_mngt"),
        'PASSWORD': env("RIT_PASSWORD", default="Epassw0rdRit"),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': env.int("CONN_MAX_AGE", default=60)  # noqa F405
    }
}

# Celery
# ------------------------------------------------------------------------------

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = ("x-requested-with", "content-type", "accept", "origin", "authorization", "x-csrftoken")

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'SIGNING_KEY': env('SIMPLE_JWT_SIGNING_KEY', default=None) or SECRET_KEY,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}
