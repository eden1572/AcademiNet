from django.shortcuts import render,get_object_or_404,redirect
from .forms import MessageForm,SolveProblemForm
from .models import Message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser,Editor
from .models import Notification
from django.http import JsonResponse

from blog.models import Post,title_exists,validate_file_extension,sizefile

def message_list(request):
    messages = Message.objects.all()#get all message arttrbutes
    return render(request,'inbox.html',{'messages':messages})

def message_detail(request,pk):
    message = get_object_or_404(Message,pk=pk)#getting the messages. pk is id.
    return render (request,'inbox_post2.html',{'message':message})

# def message_review(request):
#     if request.method =='POST':
#         sender = request.user
#         receiver =  CustomUser.objects.filter(is_superuser=True).first()#first admin

#         Message.objects.create(
#             sender=request.user,
#             receiver=receiver,
#             subject=,
#             body=message_content
#         ) 

def create_message(request):#creating messages.
    if request.method == 'POST':
        if request.method == 'POST':
            title = request.POST.get('title')
            body = request.POST.get('Description')
            topic = request.POST.get('divison')
            sender = request.user
            file_sumbit_upload = request.FILES.get('file')
            receiver = CustomUser.objects.filter(is_superuser=True).first()
            superusers = CustomUser.objects.filter(is_superuser=True)
        if file_sumbit_upload:
                validate_file_extension(file_sumbit_upload)
                sizefile(file_sumbit_upload)

        if title and body and topic and sender:
            for admin_user in superusers:
                    post = Message.objects.create(
                        subject=title,
                        receiver=admin_user,
                        body=body,
                        title_message=topic,
                        sender=sender,
                        file_sumbit_upload=file_sumbit_upload
                    )
            #send notification to admin
            superusers = CustomUser.objects.filter(is_superuser=True)
            for admin_user in superusers:
                
                Notification.objects.create(
                        user=admin_user,
                        message=f"You have received a new message from {request.user}"
                    )
            return JsonResponse({"success": True, "message": "Message have been send"})
            #return redirect('contact_us')
        else:
            return JsonResponse({"success": False, "message": "Post not saved: Missing required fields"}, status=400)
    else:
         print('hello')
         form = MessageForm()
    return render(request, 'contact_us.html', {'form': form})

def create_message_editor(request):#creating messages.
    if request.method == 'POST':
        if request.method == 'POST':
            title = request.POST.get('title')
            body = request.POST.get('Description')
            topic = request.POST.get('divison')
            sender = request.user
            file_sumbit_upload = request.FILES.get('file')
            receiver = CustomUser.objects.filter(is_superuser=True).first()
            superusers = CustomUser.objects.filter(is_superuser=True)
        if file_sumbit_upload:
                validate_file_extension(file_sumbit_upload)
                sizefile(file_sumbit_upload)

        if title and body and topic and sender:
            for admin_user in superusers:
                    post = Message.objects.create(
                        subject=title,
                        receiver=admin_user,
                        body=body,
                        title_message=topic,
                        sender=sender,
                        file_sumbit_upload=file_sumbit_upload
                    )
            #send notification to admin
            superusers = CustomUser.objects.filter(is_superuser=True)
            for admin_user in superusers:
                
                Notification.objects.create(
                        user=admin_user,
                        message=f"You have received a new message from {request.user}"
                    )
            return JsonResponse({"success": True, "message": "Message have been send"})
            #return redirect('contact_us')
        else:
            return JsonResponse({"success": False, "message": "Post not saved: Missing required fields"}, status=400)
    else:
         print('hello')
         form = MessageForm()
    return render(request, 'contact_us_editor.html', {'form': form})


def create_message_admin(request):#creating messages.
    if request.method == 'POST':
        if request.method == 'POST':
            title = request.POST.get('title')
            body = request.POST.get('Description')
            topic = request.POST.get('divison')
            sender = request.user
            file_sumbit_upload = request.FILES.get('file')
            receiver = CustomUser.objects.filter(is_superuser=True).first()
            superusers = CustomUser.objects.filter(is_superuser=True)
        if file_sumbit_upload:
                validate_file_extension(file_sumbit_upload)
                sizefile(file_sumbit_upload)

        if title and body and topic and sender:
            for admin_user in superusers:
                    post = Message.objects.create(
                        subject=title,
                        receiver=admin_user,
                        body=body,
                        title_message=topic,
                        sender=sender,
                        file_sumbit_upload=file_sumbit_upload
                    )
            #send notification to admin
            superusers = CustomUser.objects.filter(is_superuser=True)
            for admin_user in superusers:
                
                Notification.objects.create(
                        user=admin_user,
                        message=f"You have received a new message from {request.user}"
                    )
            return JsonResponse({"success": True, "message": "Message have been send"})
            #return redirect('contact_us')
        else:
            return JsonResponse({"success": False, "message": "Post not saved: Missing required fields"}, status=400)
    else:
         print('hello')
         form = MessageForm()
    return render(request, 'contact_us_admin.html', {'form': form})



def solve_problem(request, message_id):#sending a message to user when problem has been fixed.
    message = get_object_or_404(Message, pk=message_id)

    if request.method == 'POST':
        form = SolveProblemForm(request.POST, instance=message)
        if form.is_valid():
            form.problem_solved = True
            #making what was an issue no more.
            form.save()

            # Send a message back to the user
            Message.objects.create(
                sender=request.user,
                receiver=message.sender,
                subject="Your problem has been solved",
                body="Your problem has been successfully solved. If you have any further questions, feel free to ask."
            )
            
            # Create a notification for the user
            Notification.objects.create(
                user=message.sender,
                message="Your problem has been solved. Check your messages for details."
            )

            return redirect('inbox_post2', pk=message_id)  # Redirect to message detail page
    else:
        form = SolveProblemForm(instance=message)
    
    return render(request, 'solve_problem.html', {'form': form})

#notifcations
def generate_notification(user, message):
    Notification.objects.create(user=user, message=message)
    

def mark_notification_as_read(request):
     if request.method == 'POST':
        notification_ids = request.POST.getlist('notifications')
        notifications = Notification.objects.filter(id__in=notification_ids)
        for notification in notifications:
            notification.read = True
            notification.save()
     try:
        editor = Editor.objects.get(user=request.user)#checks if the user is editor.
        return redirect('editor_profile')  # Redirect to editor's profile.
     except Editor.DoesNotExist:
        return redirect('student_profile')  # Redirect to student's profile.


def user_notifactions(request):
    # Retrieve notifications for the current user
    notifications = Notification.objects.filter(user=request.user, read=False)
    return notifications

def all_users_notifactions(request):
    notifications = Notification.objects.filter(user=request.user)
    print(notifications)  # Print notifications for debugging
    return render(request, 'notifactions_list.html', {'notifications': notifications})