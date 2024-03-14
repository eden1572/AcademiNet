<<<<<<< Updated upstream
from .import views 
from django.urls import path #path helps with connetting between pages.
from .views import PostDetail 
from .views import AddPostView

urlpatterns =[
    path('blog/',views.PostList.as_view(), name = 'homeBlog'),#home page.
    #path('<slug:slug>/',views.PostDetail.as_view(),name= 'post_detail'),#blog 
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),#comments.
    path('add_post/', AddPostView.as_view(), name='add_post'),#adding a post.
    #path('post/<slug:slug>/comment', post_detail, name='post_detail'),

=======
from .import views 
from django.urls import path #path helps with connetting between pages.
from .views import PostDetail 
from .views import AddPostView 

urlpatterns =[
    path('blog/',views.PostList.as_view(), name = 'homeBlog'),#home page.
   # path('post/', views.post_detail, name='post_detail'),#.
    path('add_post/', AddPostView.as_view(), name='add_post'),#adding a post.
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
>>>>>>> Stashed changes
]