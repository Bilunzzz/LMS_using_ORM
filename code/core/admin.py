from django.contrib import admin
from core.models import Course, CourseContent, Comment, CourseMember

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'teacher')
    search_fields = ('name', 'description', 'teacher__username')

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id', 'video_url', 'created_at')
    search_fields = ('name', 'course_id__name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_id', 'user_id', 'comment', 'created_at')
    search_fields = ('content_id__name', 'user_id__username', 'comment')

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'user_id', 'roles', 'created_at')
    search_fields = ('course_id__name', 'user_id__username', 'roles')
