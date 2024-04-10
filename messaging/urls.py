from .import views 

from django.urls import path #path helps with connetting between pages.

# urlpatterns =[
#     path('blog/',views.PostList.as_view(), name = 'homeBlog'),#home page.
#     path('post/', views.post_detail, name='post_detail'),#comments.
#     path('add_post/', AddPostView.as_view(), name='add_post'),#adding a post.
#     #path('post/<slug:slug>/comment', post_detail, name='post_detail'),

# ]

urlpatterns =[
    path('messages/', views.message_list, name='inbox'),
    path('messages/<int:pk>/', views.message_detail, name='inbox_post2'),
    path('messages/create/', views.create_message, name='create_message'),
    path('notifactions_list/', views.all_users_notifactions, name='notifations_list'),
    path('solve-problem/<int:message_id>/', views.solve_problem, name='solve_problem'),
    #path('Reviews/',views.create_review,name = 'reviews')          
]