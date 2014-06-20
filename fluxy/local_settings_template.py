# /fluxy/local_settings_commented.py
# THESE SETTINGS ARE FOR THE DEV ENVIRONMENT

# !!!!!!!! ON YOUR DEV MACHINE

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

# People who get notified when errors happen
ADMINS = ()

# Media files (Images, etc.)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Store locally for local server
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
