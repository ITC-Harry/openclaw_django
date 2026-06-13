from django.contrib import admin
from .models import Project, ProjectMember


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['key', 'name', 'lead', 'project_type', 'is_active', 'created_at']
    list_filter = ['project_type', 'is_active']
    search_fields = ['name', 'key']
    inlines = [ProjectMemberInline]


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'role', 'joined_at']
    list_filter = ['role']
