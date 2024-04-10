from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from authentication.models import CustomUser
from django.utils import timezone
from datetime import timedelta

# פונקציית התצוגה לדשבורד
def dashboard_view(request):
    connected_users = CustomUser.objects.filter(last_login__gte=timezone.now() - timedelta(minutes=15)).count()
    context = {'connected_users': connected_users}
    return render(request, 'dashboard_home.html', context)

# הרחבת המחלקה AdminSite על ידי ירושה
class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        # הקריאה למתודה המקורית כדי לקבל את הנתיבים הקיימים
        urls = super().get_urls()
        # הוספת הנתיב המותאם אישית
        custom_urls = [
            path('dashboard/', self.admin_view(dashboard_view), name='dashboard')
        ]
        # החזרת הנתיבים החדשים ביחד עם הנתיבים הקיימים
        return custom_urls + urls

# יצירת אובייקט של המחלקה החדשה
my_admin_site = MyAdminSite(name='myadmin')
