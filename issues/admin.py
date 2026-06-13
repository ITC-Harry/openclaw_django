from django.contrib import admin
from .models import IssueType, IssuePriority, IssueStatus, Issue, Comment


@admin.register(IssueType)
class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']


@admin.register(IssuePriority)
class IssuePriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'color']
    list_editable = ['level']


@admin.register(IssueStatus)
class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_default', 'is_closed', 'color']
    list_editable = ['order']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'text', 'created_at']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'summary', 'status', 'priority',
                    'assignee', 'created_at']
    list_filter = ['status', 'priority', 'issue_type', 'project']
    search_fields = ['summary', 'description']
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['issue', 'author', 'created_at']
