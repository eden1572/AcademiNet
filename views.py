
from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView ,UpdateView
from .models import Post,title_exists,validate_file_extension,sizefile
from messaging.models import Notification
from .forms import CommentForm , PostForm ,PostSearchForm,RemovalRequestForm,StudyGroupForm
from django.shortcuts import render, get_object_or_404 , redirect
from django.http import FileResponse
from django.http import JsonResponse
from .models import models,RemovalRequest,StudyGroups,GroupMembers,Comment
from authentication.models import Editor,CustomUser
from messaging.views import user_notifactions
from django.contrib.auth import get_user_model
from django.contrib import messages
from messaging.models import Message
from django.db.models import Q

#Blog Views.de                                              
class PostList(generic.ListView):#makingg a list of obj of forms(Questions page)
    queryset = Post.objects.order_by('-created_on')
    template_name = 'Forum.html'#here will be the url for our html.
    context_object_name = 'post_list'

    def get_queryset(self):#Search bar, with filters
        
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        topic = self.request.GET.get('topic')
        department = self.request.GET.get('department')
        
        if query:
            queryset = queryset.filter(title__icontains=query)
        if topic:
            queryset = queryset.filter(Topic_choice=topic)
        if department:
            queryset = queryset.filter(department_choices=department)
            
        return queryset



     

class PostDetail(generic.DetailView):#detail of the obj form
    model = Post
    template_name = 'Post.html'
    
    
class AddPostView(CreateView,LoginRequiredMixin):
    model = Post
    template_name = 'question_page.html'
    fields = ('title','Topic_choice','content','header_image','department_choices')

def benefits_view(request):#getting benefits.html
    post_list = Post.objects.all()  # Or any filter/query you need

    # Pass the post_list to the template as context data
    context = {
        'post_list': post_list}

    # Render the template with the context data
    return render(request, 'benefits.html', context)
    
def reserve_view(request):
    post_list = Post.objects.all()  # Or any filter/query you need

    # Pass the post_list to the template as context data
    context = {
        'post_list': post_list}

    # Render the template with the context data
    return render(request, 'reserve.html', context)    

def some_viewstudent(request):
    post_list_users = Post.objects.all()
    user_notifications_data = user_notifactions(request)  # Call the function to get the data

    return render(request, 'student_profile.html', { 'user_notifications': user_notifications_data,'post_list': post_list_users,})

def some_vieweditor(request):
    post_list_users = Post.objects.all()
    user_notifications_data = user_notifactions(request)  # Call the function to get the data

    return render(request, 'editor_profile.html', { 'user_notifications': user_notifications_data,'post_list': post_list_users,})


def editorspost(request):
    post_list_userse = Post.objects.all()
    editor_posts = [] # List to store editor's posts
    editors = Editor.objects.all()

    # Retrieve search query and topic from the request
    query = request.GET.get('query')
    benefits_rights_choices = request.GET.get('benefits_rights_choices')

    if query:
        post_list_userse = post_list_userse.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    if benefits_rights_choices:
        post_list_userse = post_list_userse.filter(benefits_rights_choices=benefits_rights_choices)

    # Iterate through posts to check if the author is an editor
    for post in post_list_userse:
        for editor in editors:
            if post.author == editor.user:
                editor_posts.append(post)
    return render(request, 'studentsrights.html', {'post_list': editor_posts})
      

#adding posts.
@login_required
def add_post(request): 
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content') 
            division = request.POST.get('divison') 
            topic = request.POST.get('topic')
            if 'is_anonymous' in request.POST:
                post.is_anonymous = True
            author = request.user
            header_image = request.FILES.get('file')
             
            if title_exists(title):
                return JsonResponse({"success": False, "message": "Title is already taken"}, status=400)

            if header_image:
                validate_file_extension(header_image)
                sizefile(header_image)

            if title and content and topic and author:
                
                post = Post.objects.create(
                    title=title,
                    content=content,
                    department_choices=division,
                    Topic_choice=topic,
                    author=author,
                    header_image=header_image,
                )
                return redirect('homeBlog')            
            else:
                errors = form.errors.as_data()  # gets errors.
                error_messages = {}  # making an "array of errors"
                for field, error_list in errors.items():
                        error_messages[field] = [error.message for error in error_list]
                return JsonResponse({"success": False, "message": "Post not saved:","errors": error_messages},status =400)
        else:   
              form = PostForm()
        return render(request, 'question_page.html', {'form': form})

def add_post_rights(request): #only editors will make this kind of posts.
      if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')  
        topic = request.POST.get('benefits_rights_choices')
        author = request.user
        header_image = request.FILES.get('header_image')

        if title and content and topic and author:
            post = Post.objects.create(
                title=title,
                content=content,
                benefits_rights_choices=topic,
                author=author,
                isright=True,
                header_image=header_image
            )
            return redirect('studentrights')# Redirect to studentrights but we need to make js response.
        else:
            return JsonResponse({"success": False, "message": "Post not saved: Missing required fields"}, status=400)
      else:
        return render(request, 'Add_right.html')


def add_post_benefits(request):#only for editors.
  if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')  
        topic = request.POST.get('topic')
        author = request.user
        header_image = request.FILES.get('header_image')
        author_url = request.POST.get('url_to')
        if title and content and topic and author:
            post = Post.objects.create(
                title=title,
                content=content,
                benefits_choices=topic,
                author=author,
                isbenefits=True,
                header_image=header_image,
                author_url = author_url
            )
            return redirect('studentbenefits')# Redirect to studentrights but we need to make js response.
        else:
            return JsonResponse({"success": False, "message": "Post not saved: Missing required fields"}, status=400)
  else:
        return render(request, 'Add_benefits.html')

def add_post_reserve(request):#only for editors.
  if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')  
        topic = request.POST.get('topicR')
        author = request.user
        header_image = request.FILES.get('header_image')

        if title and content and topic and author:
            post = Post.objects.create(
                title=title,
                content=content,
                reserve_choices=topic,
                author=author,
                isreserve=True,
                header_image=header_image
            )
            return redirect('reserve')# Redirect to studentrights but we need to make js response.
        else:
            return JsonResponse({"success": False, "message": "Post not saved: Missing required fields"}, status=400)
  else:
        return render(request, 'Add_reserve.html')


def download(request, id):
    obj = PostForm.objects.get(id=id)
    filename = obj.model_attribute_name.path
    response = FileResponse(open(filename, 'rb'))
    return response


#Comments views.

@login_required
def post_detail(request, slug):
    template_name = 'Post.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None  # Initialize new_comment
    comment_form = CommentForm()
    if request.method == 'POST':
        
        # if comment_form.is_valid():
        #     new_comment = comment_form.save(commit=False)
        #     new_comment.post = post
        #     new_comment.name = request.user
        #     if 'file_comment_upload' in request.FILES:  # Check if 'file_comment_upload' is in request.FILES before accessing it
        #         new_comment.file_comment_upload = request.FILES['file_comment_upload']
        #     new_comment.save()
        body = request.POST.get('comment-text')  
        author = request.user
        file_comment_upload = request.FILES.get('file')

        

        if file_comment_upload:
                validate_file_extension(file_comment_upload)
                sizefile(file_comment_upload)

        if  body and  author:
            comment = Comment.objects.create(
                body=body,
                name=author,
                file_comment_upload=file_comment_upload,
                post = post,  
            )
            if (post.author != request.user):  # Avoid sending notification to self because you know you made it...
                notification_message = f"Your post '{post.title}' received a new comment."
                Notification.objects.create(user=post.author, message=notification_message)
            return JsonResponse({"success": True, "message": "Comment saved"})      
             
        else:
            # Form is not valid, return errors
            errors = comment_form.errors.as_data()
            error_messages = {}
            for field, error_list in errors.items():
                error_messages[field] = [error.message for error in error_list]
            return JsonResponse({"success": False, "message": "Post not saved:", "errors": error_messages}, status=400)

    return render(request, template_name, {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,        
        'comment_file': new_comment.file_comment_upload if new_comment else None,
        'slug': slug,
    })


def downloadfromcomments(request, id):
    obj = CommentForm.objects.get(id=id)
    filename = obj.model_attribute_name.path
    response = FileResponse(open(filename, 'rb'))
    return response
            

#updating posts
class UpdatePostView(UpdateView):
     model = Post
     template_name = 'update_post.html'
     fields = ['title','content']
     
     #sending to admin a message that post have been updated
     def form_valid(self, form):
        # Save the form
        response = super().form_valid(form)
        
        # Send notification to admin
        admin = CustomUser.objects.filter(is_superuser=True).first()  # Assuming you have a CustomUser model for admins
        if admin:
            notification_message = f"The post '{self.object.title}' has been edited."
            Notification.objects.create(user=admin, message=notification_message)
            messages.success(self.request, "Notification sent to admin about post edit.")

        return response

#removal 

def request_removal(request, post_id):#requesting to remove the post from admin.
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = RemovalRequestForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            RemovalRequest.objects.create(post=post, requested_by=request.user, reason=reason)

            admin_user = CustomUser.objects.filter(is_superuser=True).first()  # Assuming admin is the superuser
            if admin_user:
                Notification.objects.create(
                    user=admin_user,
                    message=f"Removal request for post '{post.title}' has been made by {request.user}."
                )

            messages.success(request, "Removal request sent to admin.")
            return redirect('studentrights')  # Redirect to the home page or wherever you want
    else:
        form = RemovalRequestForm()
    return render(request, 'request_removal.html', {'form': form})

def remove_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    
    if request.user.is_superuser:  # Ensure only superuser can remove post
        post.delete()
        
        # Send message to post author
        message_subject = "Your post has been removed"
        message_content = f"Your post '{post.title}' has been removed from the site."
        #making the message to his inbox.
        Message.objects.create(
            sender=request.user,
            receiver=author,
            subject=message_subject,
            body=message_content
        )
        #making a notification that the post was removed.
        notification_message = f"Your post '{post.title}' has been removed from the site."
        Notification.objects.create(user=author, message=notification_message)
        messages.success(request, f"Post '{post.title}' has been removed, and the author has been notified.")

    else:
        messages.error(request, "You do not have permission to remove this post.")
    
    return redirect('studentrights')  # Going back to studentsrights.

#StudyGroups
def Study_groups(request):#getting all studyGroups 
     groups = StudyGroups.objects.all()
     return render (request,'StudyGroups.html',{'groups':groups})

def create_group(request):#user creating one.
     if request.method == 'POST':
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        division = request.POST.get('division')
        group_size = request.POST.get('group_size')  # Retrieve selected group size
        
        # Save the group with the retrieved data
        group = StudyGroups.objects.create(title=title,description=description,division=division,group_size=group_size,author=request.user) 

        GroupMembers.objects.create(user=request.user, group=group)#adding the author to the group. 
        return redirect('study_groups')#redirect to main groups page
     else:
          form = StudyGroupForm()
     return render(request,'New_group.html',{'form':form})

def remove_group(request,group_id):
    group = get_object_or_404(StudyGroups, pk=group_id)
    author = group.author
    superuser = CustomUser.objects.filter(is_superuser=True).first()#the first admin in the list of admins.
    
    if request.user == author:  # Ensure only the author of the group can remove post
        group_members = group.groupmembers_set.all()#getting all the users in the group

        for member in group_members:  # Send a farewell to the members of the group
            message_content = f"The group '{group.title}' has been deleted by the admin."
            user = member.user
            sender = superuser
            message = Message(body=message_content, receiver=user,sender=sender)
            message.save()
        
        group.delete()
    return redirect('study_groups')

@login_required
def join_group(request, group_id):#join a group
    group = get_object_or_404(StudyGroups, id=group_id)
    user = request.user
    
    # Checking if the user is already a part of thy group.
    if GroupMembers.objects.filter(group=group, user=user).exists():
        messages.warning(request, 'You are already a member of this group.')
        return redirect('study_groups')  # Redirect user to study groups page or any other appropriate page
    
    # check if there is space
    if GroupMembers.objects.filter(group=group).count() > 8:#limitig to 6 people
        messages.error(request, 'This group has reached its maximum capacity.')
        return redirect('study_groups')  # Redirect user to study groups page or any other appropriate page
    
    # Adding  user to the group
    GroupMembers.objects.create(user=user, group=group)
    messages.success(request, 'You have successfully joined the group.')
    return redirect('study_groups')  # Redirect user to study groups page or any other appropriate page

