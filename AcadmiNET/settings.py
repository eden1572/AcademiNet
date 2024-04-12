from pathlib import Path
import os


# משמש ליצירת נתיבים יחסיים בתוך הפרויקט, מייצג את התיקייה הבסיסית של הפרויקט.
BASE_DIR = Path(__file__).resolve().parent.parent

#מפתח סודי שמשמש לחתימה דיגיטלית, לא לחשוף בפרודקשיין.
SECRET_KEY = 'your-secret-key'

#מצב פיתוח שמאפשר קבלת מידע על שגיאות
DEBUG = True

#רשימת ההוסטים שהאתר יכול לרוץ עליהם
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

#רשימת אפליקציות מותקנות
INSTALLED_APPS = [
    'adminlte3',
    'adminlte3_theme',
    'django.contrib.admin',
    'admin_interface',
    'colorfield',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  
    'blog', #making the blog database.
    'crispy_forms',#for the blog form
    'authentication',#authentications.
    'django_admin_logs',
    'dashboard',
    'chartjs',
    'messaging',#messaging system
    #'django_pdb'#debugger

]

# מנגנון שמתווך בין הבקשה לתגובה במהלך עיבוד בקשה בשרת.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django_pdb.middleware.PdbMiddleware',#debugger

]


#הגדרת הנתיב לדף התחברות 
LOGIN_URL = '/signin/'
#קובץ בו מוגדרים כל נתיבי ה-URL של הפרוייקט 
ROOT_URLCONF = 'AcadmiNET.urls'

#הגדרות למערכת התבניות של DJANGO
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dashboard', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },  
    },
]

#ציון המודל של הפרויקט לצורך הרצתו כאפליקציית אינטרנט
WSGI_APPLICATION = 'AcadmiNET.wsgi.application'


#הגדרת ההגדרות של מסד הנתונים
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',        
    }
}


#רשימת מאמתי סיסמא - לוודא שהמשתמשים יוצרים סיסמאות בטוחות 
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


#זמן ברירת המחדל ואזור הזמן 
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'israel'

#תמיכה בינלאומית - מאפשר להציג את האתר בשפות שונות ע"פ דרישת המשתמש
USE_I18N = True

#מאפשר תמיכה באזורי זמן שונים - להציג תאריכים וזמנים 
USE_TZ = True

#הנתיב הבסיסי לקבצים סטטיים
STATIC_URL = '/static/'

#ניהול הקבצים שמעלים המשתמשים
MEDIA_URL = '/media/' #הנתיב הוירטואלי בו יהיו זמינים הקבצים 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')#המיקום בשרת שבו הקבצים האלה יאוחסנו

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #אוסף כל הקבצים הסטטיים
STATICFILES_DIRS = [  os.path.join(BASE_DIR, 'static'),] #התיקיות מהן יילקחו הקבצים הסטטיים

#הגדרות הנוגעות לשליחת מייל אלקטרוני
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aacademinet@gmail.com'
EMAIL_HOST_PASSWORD = 'lrceowqjycpovtjm '
# הגדרת זמן פקיעה של קישור איפוס הסיסמה ל-5 דקות
PASSWORD_RESET_TIMEOUT = 300  # 5 דקות בשניות

#סוג השדה שיווצר לכל רשימה במסד נתונים
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'authentication.CustomUser' #מאפשר להגדיר מודל משתמש אישי


# תצורת Django Admin Logs

# מאפשר מחיקת רשומות יומן מממשק האדמין
DJANGO_ADMIN_LOGS_DELETABLE = True

# מאפשר או מבטל יצירת רשומות יומן בממשק האדמין
DJANGO_ADMIN_LOGS_ENABLED = True

# מתעלם מיצירת רשומות יומן כאשר עצם לא שונה
DJANGO_ADMIN_LOGS_IGNORE_UNCHANGED = True




