from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm, SigninForm
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from .models import CustomUser, Editor
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import AdminNotification
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from .forms import EditorSignupForm
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


#דף הפרוייקט ומסך הפתיחה
def index(request):
    return render(request, "project.html")

#פונקציה המאפשרת להתחבר למערכת לכל סוגי המשתמשים. מאשרת/דוחה התחברות בהתאם לסוג המשתמש ובחירת הממשק
def signIn(request):
    if request.method == 'POST': # בדיקה האם הבקשה מצד הלקוח היא באמצעות הבקשה POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_editor = request.POST.get('is_editor') == 'true'

        # נבדוק קודם אם המשתמש הוא ADMIN או SUPERVISER
        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser:  # הבדיקה אם המשתמש הוא ADMIN
                login(request, user)
                return JsonResponse({"success": True, "message": "Admin logged in successfully", "redirect": "homepage_admin"})
            
            # נמשיך לבדוק עבור עורכים
            try:
                editor = Editor.objects.get(user__username=username)
                if is_editor:
                    if check_password(password, editor.user.password):
                        login(request, editor.user)
                        return JsonResponse({"success": True, "message": "Editor logged in successfully", "redirect": "homepage_editor"})
                    else:
                        return JsonResponse({"success": False, "message": "Incorrect password for editor"})
                else:
                    return JsonResponse({"success": False, "message": "Editor must login through the editor interface"})
            except Editor.DoesNotExist:
                if is_editor:
                    return JsonResponse({"success": False, "message": "Access denied for regular users"})
                else:
                    login(request, user)
                    return JsonResponse({"success": True, "message": "Login successful"})
        else:
            return JsonResponse({"success": False, "message": "Incorrect username or password"})

    return JsonResponse({"success": False, "message": "Invalid request"})


#פונקציה המאפשרת לסטודנט להירשם למערכת, בודק קלט ויוצר/לא יוצר משתמש בהתאם
def signUp(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"success": True, "message": "Account created successfully"})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"success": False, "message": "Error in form submission", "errors": errors})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})


#פונקציה המאפשרת לכל סוג משתמש להתנתק מהמערכת
@login_required
def signOut(request):
    logout(request)
    return redirect('project')  # הפניה לדף התחברות לאחר ההתנתקות

#פונקציה המאפשרת לאדמין להתנתק ולחזור לממשק הניהול 
@login_required
def signout_admin(request):
    # ביצוע התנתקות למשתמש הנוכחי
    logout(request)
    # הפניה לדף הבית או לדף ההתחברות לאחר ההתנתקות
    return redirect('/admin/login/')  # הפניה לדף ההתחברות של ממשק האדמין

#הגדרת דף הבית
def project(request):
    return render(request, 'project.html')


#הגדרת עמוד בית - סטודנט 
@login_required
def homepage(request):
    return render(request, 'homepage.html')


#הגדרת עמוד בית - EDITOR
@login_required
def homepage_editor(request):
    try:
        editor = request.user.editor
        return render(request, 'homepage_editor.html', {'editor': editor})
    except Editor.DoesNotExist:
        return redirect('homepage') # אם העורך לא נמצא
    
#בדיקה האם משתמש בעל הרשאות גבוהות
def is_admin_user(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin_user, login_url='/login/')
def homepage_admin(request):
    # קוד עבור הדף של ה-ADMIN
    return render(request, 'homepage_admin.html')


#פונקציה המגדירה הפניה לעמוד "קצת עלינו" לכל סוג משתמש בהתאם
@login_required
def about_us(request):
    return render(request, 'about_us.html')

@login_required
def about_us_editor(request):
    return render(request, 'about_us_editor.html')

@login_required
def about_us_admin(request):
    return render(request, 'about_us_admin.html')


#פונקציה המגדירה הפניה לעמוד "זכויות" לכל סוג משתמש בהתאם
@login_required
def rights_page(request):
    return render(request, 'rights_page.html')

@login_required
def rights_page_editor(request):
    return render(request, 'rights.html')

@login_required
def rights_page_admin(request):
    return render(request, 'rights_admin.html')

#פונקציה המגדירה הפניה לבלוג לכל סוג משתמש בהתאם
@login_required
def blog_page(request):
    return render(request, 'blog_page.html')

@login_required
def blog_page_editor(request):
    return render(request, 'blog_page_editor.html')

@login_required
def blog_page_admin(request):
    return render(request, 'blog_page_admin.html')

#פונקציה המגדירה הפניה לעמוד "צור קשר" לכל סוג משתמש בהתאם
@login_required
def contact_us(request):
    return render(request, 'contact_us.html')

@login_required
def contact_us_editor(request):
    return render(request, 'contact_us_editor.html')

@login_required
def contact_us_admin(request):
    return render(request, 'contact_us_admin.html')


#פונקציה המאפשרת למשתמש לאפס סיסמא באמצעות שליחת מייל
@login_required
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        form = PasswordResetForm({'email': email})
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='emails/password_reset_email.html',
                subject_template_name='emails/password_reset_subject.txt',
                from_email='aacademinet@gmail.com'
            )
            messages.success(request, "Instructions to reset your password have been sent to your email.")
            return redirect('password_reset_done')
        else:
            messages.error(request, "Error with form submission.")
    else:
        form = PasswordResetForm()

    return render(request, 'forgotpassword.html', {'form': form})


#הגדרת פונקציות לניתובים לטובת איפוס סיסמא באמצעות טופס DJANGO המובנה
@login_required
def password_reset(request):
    return render(request, 'password_reset_form.html')

@login_required
def password_reset_complete(request):
    # View function for rendering the password reset complete page.
    return render(request, 'password_reset_complete.html')


#הגדרת פונקציות הפרופיל עבור השמתמש 
@login_required
def student_profile(request):
    # המשתמש המחובר זמין דרך request.user
    return render(request, 'student_profile.html', {'user': request.user})

@login_required
def editor_profile(request):
    try:
        editor = request.user.editor
        return render(request, 'editor_profile.html', {'editor': editor})
    except Editor.DoesNotExist:
        return redirect('homepage') #אם העורך לא נמצא 

@login_required
def admin_profile(request):
    if request.user.is_superuser:  # בדיקה אם המשתמש הוא 'ADMIN'
        return render(request, 'admin_profile.html', {'admin': request.user})
    

#הגדרת פונקציה לשינוי מייל של משתמש סטודנט 
@login_required
def change_email_student(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        if new_email:
            user = request.user
            if user.email == new_email:
                return JsonResponse({'success': False, 'message': 'This email is already in use.'})
            user.email = new_email
            user.save()
            return JsonResponse({'success': True, 'message': 'Email changed successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Please enter a new email.'})
    elif request.method == 'GET':
        # Render the HTML page for GET request
        return render(request, 'change_email_student.html', {'user': request.user})
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)
    

#הגדרת פונקציה לשינוי מייל של משתמש עורך 
@login_required
def change_email_editor(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        if new_email:
            user = request.user
            if user.email == new_email:
                return JsonResponse({'success': False, 'message': 'This email is already in use.'})
            user.email = new_email
            user.save()
            return JsonResponse({'success': True, 'message': 'Email changed successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Please enter a new email.'})
    elif request.method == 'GET':
        # Render the HTML page for GET request
        return render(request, 'change_email_editor.html', {'user': request.user})
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)


#הגדרת פונקציה לשינוי סיסמא של משתמש עורך 
@login_required
def change_password_editor(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            redirect_url = '/authentication/editor-profile/'
            return JsonResponse({'success': True, 'message': 'Password changed successfully.', 'redirect_url': redirect_url})
        else:
            errors = "; ".join(["%s: %s" % (field, error[0]) for field, error in form.errors.items()])
            return JsonResponse({'success': False, 'message': 'Failed to change the password: ' + errors})
    else:  # GET request
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password_editor.html', {'form': form})


#הגדרת פונקציה לשינוי סיסמא של משתמש סטודנט 
@login_required
def change_password_student(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            redirect_url = '/authentication/student-profile/'
            return JsonResponse({'success': True, 'message': 'Password changed successfully.', 'redirect_url': redirect_url})
        else:
            errors = "; ".join(["%s: %s" % (field, error[0]) for field, error in form.errors.items()])
            return JsonResponse({'success': False, 'message': 'Failed to change the password: ' + errors})
    else:  # GET request
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password_student.html', {'form': form})


#הגדרת פונקציה לשינוי טלפון - רלוונטי רק ל-EDITOR 
@login_required
def change_phone(request):
    if request.method == 'POST':
        new_phone = request.POST.get('new_phone')
        if new_phone:
            editor = request.user.editor
            if editor:
                if editor.phone == new_phone:
                    return JsonResponse({'success': False, 'message': 'This Phone is already in use.'})
                editor.phone = new_phone
                editor.save()
                return JsonResponse({'success': True, 'message': 'Phone changed successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'User is not an editor.'})
        else:
            return JsonResponse({'success': False, 'message': 'Please enter a new phone.'})
    elif request.method == 'GET':
        # Render the HTML page for GET request
        return render(request, 'change_phone.html', {'user': request.user})
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)


#שליחת מייל לאחר שמישהו מגיש בקשה להצטרף ל-EDITOR
User = get_user_model()
def send_approval_request_to_admin(editor):
    if editor.user:
        AdminNotification.objects.create(
            message=f"New editor signup request from {editor.user.username}. Please review and approve."
        )
    else:
        # Handle case where there is no user linked to the editor
        print("Error: Editor object does not have a linked user.")


#הגדרת פונקציית ההרשמה לעורך לאתר (השארת פרטים ובמידת הצורך האדמין יוצר איתו קשר ויוצר לו משתמש בהתאם) 
def editor_signup(request):
    if request.method == 'POST':
        form = EditorSignupForm(request.POST, request.FILES)
        if form.is_valid():
            editor = form.save()
            return JsonResponse({'success': True, 'redirect_url': '/project/'})        
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = EditorSignupForm()
    return render(request, 'signup_editor.html', {'form': form})


#הגדרת הפונקציות של תתי ההפניות בעמוד זכויות
@login_required
def student_rights(request):
    return render(request, 'studentrights.html')

@login_required
def reserve_personal(request):
    return render(request, 'reservepersonal.html')

@login_required
def benefit(request):
    return render(request, 'benefit.html')