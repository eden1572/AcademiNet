<<<<<<< Updated upstream
from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','status','created_on')
    list_filter = ("status",)#filter for the status.
    search_fields = ['title','content']#making a search mode.
    prepopulated_fields = {'slug':('title',)}
    
    summernote_fields = ("content",)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Post,PostAdmin)#registering admin.
=======
from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','header_image','department_choices')
   # list_filter = ("status",)#filter for the status.
    search_fields = ['title','content']#making a search mode.
   # prepopulated_fields = {'slug':('title',)}
    
    summernote_fields = ("content",)

    def approve_comments(self, request, queryset):
        queryset.update(active=True)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Post,PostAdmin)#registering admin.
>>>>>>> Stashed changes
admin.site.register(Comment, CommentAdmin)#registering to the admin.