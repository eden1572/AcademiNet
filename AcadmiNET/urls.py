"""
URL configuration for AcadmiNET project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings#felix-files uploads
from django.conf.urls.static import static
from authentication import views as auth_views#eden- users.

#הוספתי פה 
from django.urls import path, re_path #זה אומר תביא לי את URL שמאפשר לעשות אותו דבר כמו PATH
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< Updated upstream
    #path(r'^admin',include(admin.urls)) #לא לשכוח לטפל בנתיב
]
=======
    path('', include('blog.urls')),
    path('',include('authentication.urls')),
    #path('signup/', auth_views.signUp, name='signup'),  # נתיב להרשמה
    #path('signin/', auth_views.signIn, name='signin'),  # נתיב להתחברות
   # path('signout/', auth_views.signOut, name='signout'),
    

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
>>>>>>> Stashed changes
