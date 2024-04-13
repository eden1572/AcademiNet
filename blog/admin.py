from django.contrib import admin
from .models import Post, Comment,StudyGroups,GroupMembers
from messaging.models import  Message



class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','header_image','department_choices')
   # list_filter = ("status",)#filter for the status.
    search_fields = ['title','content']#making a search mode.
   # prepopulated_fields = {'slug':('title',)}
    actions = ['remove_and_notify']
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

class StudyGroupsadmin(admin.ModelAdmin):
    list_display = ('title','description','division','data_created','group_size','author')
    list_filter = ('division', 'group_size')
    search_fields = ['title', 'author']

class GroupMembersadmin(admin.ModelAdmin):
    list_display = ('user','Group_name','join_date','left_date')
    list_filter = ('group',)
    ordering = ['join_date']

    def Group_name(self, obj):
        return obj.group.title if obj.group else '-'  # Check if group is None to avoid AttributeError


admin.site.register(GroupMembers,GroupMembersadmin)#registering group members
admin.site.register(StudyGroups,StudyGroupsadmin)#registering study groups
admin.site.register(Post,PostAdmin)#registering admin.
admin.site.register(Comment, CommentAdmin)#registering to the admin.