from .import views 
from django.urls import path #path helps with connetting between pages.
from .views import PostDetail 
from .views import AddPostView , UpdatePostView,post_detail,remove_post,add_post_benefits
from django.conf.urls.static import static
from messaging.views import mark_notification_as_read
from django.conf import settings

# urlpatterns =[
#     path('blog/',views.PostList.as_view(), name = 'homeBlog'),#home page.
#     path('post/', views.post_detail, name='post_detail'),#comments.
#     path('add_post/', AddPostView.as_view(), name='add_post'),#adding a post.
#     #path('post/<slug:slug>/comment', post_detail, name='post_detail'),
         #path('blog/',views.PostList.as_view(), name = 'homeBlog'),#home page.
# ]

urlpatterns =[

    path('blog/',views.PostList.as_view(), name = 'homeBlog'),#home page.
    path('blog/post/', views.post_detail, name='post_detail'),#.
    path('blog/add_post/', views.add_post, name='add_post'),#adding a post.
    path('blog/post/<slug:slug>/', views.post_detail, name='post_detail'),#comments
    path('blog/post/<slug:slug>/edit',UpdatePostView.as_view(), name = 'update_post'),#editiong posts.
    path('blog/check_valid/',views.add_post, name='check_valid'),
    path('blog/check_valid_comments/',views.post_detail, name ='check_valid_comments'),
    path('blog/studentrights/',views.editorspost, name = 'studentrights'),#posts for students rights.
    path('blog/messages/<int:post_id>/request_removal/', views.request_removal, name='request_removal'),
    path('blog/messages/<int:post_id>/request_removal_benefits/',views.request_removal_benefits,name = 'request_removal_benefits'),
    path('blog/remove-post/<int:post_id>/', remove_post, name='remove_post'),
    path('blog/mark-notifications-as-read/', mark_notification_as_read, name='mark_notifications_as_read'),
    path('blog/studyGroups/',views.Study_groups, name = 'study_groups'),
    path('blog/join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('blog/create_group/',views.create_group,name = 'create_group'),
    path('blog/delete_group/<int:group_id>',views.remove_group, name = 'delete_group'),
    path('blog/add_benefits/',views.add_post_benefits,name ='Add_benefits'),
    path('blog/add_right/',views.add_post_rights,name = 'Add_right'),
    path('blog/studentbenefits/',views.benefits_view, name = 'studentbenefits'),
    path('blog/reserve/',views.reserve_view, name = 'reserve'),
    path('blog/add_reserve/',views.add_post_reserve,name = 'Add_reserve'),
    path('Events/',views.allevents,name='Events'),
    path('Workshops/',views.allWorkshops,name='Workshops'),
    path('Scholarships/',views.allScholarships,name='Scholarships'),
]

urlpatterns +=  static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)