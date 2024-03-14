<<<<<<< Updated upstream

from django.views import generic
from django.views.generic import CreateView
from .models import Post
from .forms import CommentForm , PostForm 
from django.shortcuts import render, get_object_or_404 , redirect

#Blog Views.
class PostList(generic.ListView):#makingg a list of obj of forms.
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'#here will be the url for our html.
    context_object_name = 'post_list'

class PostDetail(generic.DetailView):#detail of the obj form
    model = Post
    template_name = 'post_detail.html'

class AddPostView(generic.CreateView):
    model = Post
    template_name = 'add_post.html'
    fields = '__all__'


def index(request):
    return render(request,'index.html',context=None)


#Comments views.

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None  # Initialize new_comment

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)#building comment(we don't save it yet)
            new_comment.post = post#saving in the right post.
            new_comment.save()#save the post
            
    else:
        comment_form = CommentForm()

    return render(request, template_name, {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })




=======
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .models import Post
from .forms import CommentForm , PostForm 
from django.shortcuts import render, get_object_or_404 , redirect

#Blog Views.
class PostList(generic.ListView):#makingg a list of obj of forms.
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index1.html'#here will be the url for our html.
    context_object_name = 'post_list'

class PostDetail(generic.DetailView):#detail of the obj form
    model = Post
    template_name = 'post_detail.html'
    
class AddPostView(CreateView):
    model = Post
    template_name = 'question_page.html'
    #form_class = PostForm
    #success_url = reverse_lazy('homeBlog')
    fields = ('title','content','header_image','department_choices')

    def add_post(request):
        if request.method == 'POST':
         form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homeBlog')  
        else:
            form = PostForm()
        return render(request, 'base.html', {'form': form})
    
    # def index(request):
    #     return render(request,'index.html',context=None)


#Comments views.

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None  # Initialize new_comment

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)#building comment(we don't save it yet)
            new_comment.post = post#saving in the right post.
            new_comment.save()#save the post
            
    else:
        comment_form = CommentForm()

    return render(request, template_name, {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })




>>>>>>> Stashed changes
            