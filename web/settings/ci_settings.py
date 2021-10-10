from .settings import *

SITE_ID=1

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'sqlite3.db',
            }
        }

DJANGO_DRF_FILEPOND_UPLOAD_TMP = str(BASE_DIR / 'fixtures')
