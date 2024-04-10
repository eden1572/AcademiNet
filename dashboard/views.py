from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from blog.models import Post,StudyGroups
from messaging.models import Message
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_home(request):
    if not request.user.is_superuser:
        return redirect('home')  # החלף 'home' בנתיב הרצוי

    connected_users = CustomUser.objects.filter(last_login__gte=timezone.now() - timedelta(minutes=15)).count()
    connected_users_list = CustomUser.objects.filter(last_login__gte=timezone.now() - timedelta(minutes=15))
    connected_users_count = connected_users_list.count()
    recent_logins = CustomUser.objects.filter(last_login__gte=timezone.now() - timedelta(days=7)).count()
    amount_posts = Post.objects.all().count()#all posts
    amount_Studygroups =StudyGroups.objects.all().count()#all active Study Groups
    amount_problem = Message.objects.filter(problem_solved=False,issue=True).count()#counting the amount of msg that weren't fixed
    amount_fixed_problems = Message.objects.filter(problem_solved = True,issue=True).count()#takes the msg that aren't issues.
    context = {
        'connected_users': connected_users_count,
        'recent_logins': recent_logins,
        'users_list': connected_users_list,
        'amount_posts':amount_posts,
        'amount_Studygroups':amount_Studygroups,
        'amount_problem':amount_problem,
        'amount_fixed_problems':amount_fixed_problems,
    }
    
    return render(request, 'dashboard_home.html', context)
