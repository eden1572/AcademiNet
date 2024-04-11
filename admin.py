from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from datetime import timedelta #עבודה עם פרקי זמן
from django.contrib.auth.hashers import make_password #פונקציה שמשמשת להצפנת סיסמאות
from django.utils.html import mark_safe #מניעת XSS 
from django.core.mail import send_mail
from .models import CustomUser, Editor, AdminNotification
from django.utils.html import format_html


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('display_username_with_profile_picture', 'email', 'is_staff', 'is_superuser', 'is_currently_active', 'is_active_last_7_days')
    search_fields = ('username', 'email')

    #משתמש פעיל בזמן האחרון/במהלך שבעת הימים האחרונים
    def is_currently_active(self, obj):
        return obj.last_activity >= timezone.now() - timedelta(minutes=5)
    is_currently_active.boolean = True
    is_currently_active.short_description = 'Currently Active'

    def is_active_last_7_days(self, obj):
        return obj.last_activity >= timezone.now() - timedelta(days=7)

    is_active_last_7_days.boolean = True
    is_active_last_7_days.short_description = 'Active in last 7 days'


    def display_username_with_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">{}'.format(obj.profile_picture.url, obj.username))
        else:
            # Use a default profile picture if the user doesn't have one
            default_profile_picture_url = 'https://turag.co.il/wp-content/uploads/2018/06/man.jpg'  # URL of the default profile picture
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">{}'.format(default_profile_picture_url, obj.username))

    display_username_with_profile_picture.short_description = 'Username'


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'profile_picture', 'academic_institution', 'department', 'year')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_activity')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'profile_picture', 'academic_institution', 'department', 'year')}),
    )

#רישום המחלקה בממשק אדמין
admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'created_at', 'is_treated'] #שדות שיוצגו ברשימת ההתרעות 
    list_filter = ['is_treated'] 
    actions = ['mark_as_treated', 'send_notification'] #פעולות ניהול 

    def picture_preview(self, obj):
        if obj.picture:
            return mark_safe('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.picture.url)) #הצגת HTML בטוח
        else:
            return None

    picture_preview.short_description = 'Image Preview'

    def mark_as_treated(self, request, queryset):
        queryset.update(is_treated=True)

    mark_as_treated.short_description = "Mark selected notifications as treated"

    def send_notification(self, request, queryset):
        treated_notifications = queryset.values_list('message', flat=True)
        users_to_notify = queryset.values_list('user__email', flat=True)
        send_mail(
            'Notification Treated',
            f'The following notifications have been marked as treated: {", ".join(treated_notifications)}',
            'aacademinet@gmail.com',
            users_to_notify,
            fail_silently=False,
        )

    send_notification.short_description = "Send notification to users"


admin.site.index_template = 'admin/base.html'
# admin.site.index_template = 'admin/graph_test.html'


#ניהול עורכים
class EditorAdmin(admin.ModelAdmin):
    list_display = ['display_username_with_profile_picture', 'phone', 'organization_name', 'role_in_organization', 'is_approved', 'get_user_email']
    search_fields = ['full_name', 'phone', 'organization_name', 'role_in_organization', 'user__email', 'user__username'] #חיפוש בפרטים שונים של העורך
    actions = ['approve_editor','delete_editor']  # הוספת פעולת מחיקה 

   
    def display_username_with_profile_picture(self, obj):
        if obj.user and obj.user.profile_picture:
            profile_picture = '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 5px;">'.format(obj.user.profile_picture.url)
        else:
            # ניתן להחליף כאן לכתובת של תמונת ברירת מחדל שלך
            default_profile_picture_url = 'https://turag.co.il/wp-content/uploads/2018/06/man.jpg'  
            profile_picture = '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 5px;">'.format(default_profile_picture_url)

        username = obj.user.username if obj.user else ''
        return format_html(profile_picture + '{}', username)

    display_username_with_profile_picture.short_description = 'User and Picture'

    def approve_editor(self, request, queryset): #אישור עורכים נבחרים
        queryset.update(is_approved=True)

    approve_editor.short_description = "Approve selected editors"

    def get_user_email(self, obj): #כתובת הדוא"ל ושם המשתמש המקושר לעורך
        return obj.user.email if obj.user else None

    get_user_email.short_description = 'Email'

    def get_user_username(self, obj):
        return obj.user.username if obj.user else None

    get_user_username.short_description = 'Username'

    def save_model(self, request, obj, form, change):
        if obj.user:
            obj.user.password = make_password(obj.user.password)
        super().save_model(request, obj, form, change)

    # הוספת העמודה לעריכה בממשק האדמין
    def is_approved(self, obj):
        return obj.is_approved

    is_approved.boolean = True
    is_approved.short_description = 'Approved'

    # פעולת מחיקה
    def delete_editor(self, request, queryset):
        for editor in queryset:
            user = editor.user
            if user:
                user.delete()
            editor.delete()

admin.site.register(Editor, EditorAdmin)
