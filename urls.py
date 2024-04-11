from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from blog.views import PostList, some_viewstudent



#from blog.views import PostList 
print(settings.MEDIA_ROOT)

urlpatterns = [
     
    path('', views.project, name='project'),#הגדרת עמוד הפתיחה של האתר
    path('signin/', views.signIn, name='signin'), #ניתוב לעמוד התחברות 
    path('signup/', views.signUp, name='signup'), #ניתוב לעמוד הרשמה
    path('signout/', views.signOut, name='signout'), #ניתוב לעמוד התנתקות 
    path('logout/', views.signout_admin, name='logout'), #התנתקות ADMIN
    path('homepage/', views.homepage, name='homepage'), #עמוד הבית של הסטודנט
    path('homepage_editor/', views.homepage_editor , name='homepage_editor'),#עמוד בית עורך 
    path('homepage_admin/', views.homepage_admin , name='homepage_admin'),#עמוד בית ADMIN

    path('forgot-password/', views.forgot_password, name='forgot-password'), #ניתוב לשחזור סיסמא מחוץ לממשק

    #ניתוב לעמוד "קצת עלינו" עבור כל משתמש באתר
    path('about_us/', views.about_us, name='about_us'),
    path('about_us_editor/', views.about_us_editor, name='about_us_editor'),
    path('about_us_admin', views.about_us_admin, name='about_us_admin'),

    #ניתוב לעמוד "זכויות" עבור כל משתמש באתר
    path('rights_page/', views.rights_page, name='rights_page'),
    path('rights_page_editor/', views.rights_page_editor, name='rights_page_editor'),
    path('rights_page_admin/', views.rights_page_admin, name='rights_page_admin'),

    #הגדרת הניתובים בתוך עמוד זכויות
    path('student-rights/', views.student_rights, name='student-rights'),
    path('reserve-personal/', views.reserve_personal, name='reserve-personal'),
    path('benefit/', views.benefit, name='benefit'),

    #ניתוב לעמוד "צור קשר" עבור כל משתמש באתר
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact_us_editor/', views.contact_us_editor, name='contact_us_editor'),
    path('contact_us_admin/', views.contact_us_admin, name='contact_us_admin'),

    #ניתוב לעמוד "בלוג" עבור כל משתמש באתר
    path('blog_page/', PostList.as_view(), name='blog_page'),
    path('blog_page_editor/',PostList.as_view(), name='blog_page_editor'),
    path('blog_page_admin/',PostList.as_view(), name='blog_page_admin'),



    # תהליך איפוס הסיסמה
  
  #נשלחת הודעת מייל עם הנושא והטקסט הרלוונטי
   path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset/password_reset_form.html',
             email_template_name='password_reset/password_reset_email.html',
             subject_template_name='password_reset/password_reset_subject.txt',
             success_url=reverse_lazy('password_reset_done')
         ), 
         name='password_reset'),

    # URL לאישור שהבקשה לאיפוס סיסמה נשלחה
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/password_reset_done.html'
         ), 
         name='password_reset_done'),

    #URL לאישור בקשת איפוס הסיסמא, והזנת הפרטים
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete') 
        ), 
        name='password_reset_confirm'),

    # URL לאישור שהסיסמה שונתה בהצלחה
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

  
    #הגדרת עמוד פרופיל עבור כל משתמש באתר
    path('student-profile/', views.student_profile, name='student_profile'),
    path('editor-profile/', views.editor_profile, name='editor_profile'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),

    #ביצוע שינויים בעמוד הפרופיל האישי כגון - מייל, טלפון וסיסמא עבור המשתמשים
    path('change-email-student/', views.change_email_student, name='change-email-student'),
    path('change-email-editor/', views.change_email_editor, name='change-email-editor'), 
    path('change-phone/', views.change_phone, name='change-phone'),
    path('change-password-editor/', views.change_password_editor, name='change-password-editor'),
    path('change-password-student/', views.change_password_student, name='change-password-student'),

    #עמוד הרשמה לעורך
    path('editor_signup/', views.editor_signup, name='editor_signup'),
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #הוספת נתיבים לשירות קבצים סטטיים וקבצי מדיה 
