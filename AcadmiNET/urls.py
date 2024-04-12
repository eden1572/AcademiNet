from django.contrib import admin
from django.urls import include, path
from authentication import views as auth_views #אפליקציית authentication
from django.conf.urls.static import static #ייבוא של פונקציה מובנית ב-DJANGO לשירות קבצים סטטיים
from django.conf import settings 


urlpatterns = [
    path('', auth_views.index, name='index'),  # נתיב לעמוד הבית
    path('admin/', admin.site.urls), #נתיב לממשק אדמין
    path('authentication/', include('authentication.urls')), #הגדרת נתיבי URL בתוך אפליקציית AUthentication
    path('dashboard/', include('dashboard.urls')), #הגדרת נתיבי URL בתוך אפליקציית Dashboard
    path('logout/', auth_views.signout_admin, name='logout'), #נתיב להתנתקות עבור משתמשי אדמין
    path('blog/', include('blog.urls')),#blogs.
    path('authentication/messaging/',include('messaging.urls')),#messaging



    # path('blog/', include('blog.urls')), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #הוספת נתיבים לשירות קבצים סטטיים וקבצי מדיה 



