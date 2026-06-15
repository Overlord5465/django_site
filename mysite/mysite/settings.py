from pathlib import Path
import os

                                                                
BASE_DIR = Path(__file__).resolve().parent.parent


                                                              
                                                                       

                                                                  
SECRET_KEY = 'django-insecure-s#_h_6i47wxnypknl*xv9@gx_1y8w+7j^)6hyfe6mm=ctba0%@'

                                                                 
DEBUG = True

                                                                                          
_allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "").strip()
ALLOWED_HOSTS = (
    [h.strip() for h in _allowed_hosts.split(",") if h.strip()]
    if _allowed_hosts
    else ["127.0.0.1", "localhost", "host.docker.internal"]
)


                        

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'profiles.apps.ProfilesConfig',
    'works.apps.WorksConfig',
    'topics.apps.TopicsConfig',
    'chat.apps.ChatConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'works.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


          
                                                               
 
                                                                                   
                      
                                                                                                                           

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": int(os.environ.get("POSTGRES_CONN_MAX_AGE", "0")),
    }
}


                     
                                                                              

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


                      
                                                    

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


                                        
                                                           

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

                       
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

                                               
                                                                                             
                                                                                    
ONLYOFFICE_DS_URL = os.environ.get("ONLYOFFICE_DS_URL", "http://localhost:8082").rstrip(
    "/"
)
                                                                         
                                                                                                         
ONLYOFFICE_PUBLIC_DS_URL = os.environ.get("ONLYOFFICE_PUBLIC_DS_URL", ONLYOFFICE_DS_URL).rstrip(
    "/"
)
                                                                                                                      
                                          
                                                                                   
_onlyoffice_app_public = (os.environ.get("ONLYOFFICE_APP_PUBLIC_URL") or "").strip().rstrip("/")
ONLYOFFICE_APP_PUBLIC_URL = _onlyoffice_app_public or None
                                                                
ONLYOFFICE_CALLBACK_TOKEN = os.environ.get("ONLYOFFICE_CALLBACK_TOKEN", "dev-onlyoffice-callback-token")
                                                                                         
                                                                          
_onlyoffice_jwt = os.environ.get("ONLYOFFICE_JWT_SECRET", "dev-onlyoffice-jwt-secret")
ONLYOFFICE_JWT_SECRET = "" if _onlyoffice_jwt.strip() == "" else _onlyoffice_jwt

                                
                                                                        

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@kubsu.local")
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'profiles:login'
