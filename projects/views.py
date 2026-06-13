from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Project, ProjectMember
from .forms import ProjectForm, AddMemberForm
from issues.models import Issue


@login_required
def project_list(request):
    projects = Project.objects.filter(
        models.Q(members__user=request.user) | models.Q(lead=request.user)
    ).distinct().select_related('lead').prefetch_related('issues')
    total = sum(p.issues.count() for p in projects)
    open_count = sum(p.issues.exclude(status__is_closed=True).count() for p in projects)
    done_count = sum(p.issues.filter(status__is_closed=True).count() for p in projects)
    return render(request, 'projects/list.html', {
        'projects': projects,
        'total_issues': total,
        'open_issues': open_count,
        'done_issues': done_count,
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.lead = request.user
            project.save()
            # Add creator as admin member
            ProjectMember.objects.create(
                project=project, user=request.user, role='admin'
            )
            messages.success(request, f'專案 {project.key} 建立成功！')
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/form.html', {'form': form, 'title': '建立專案'})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            'members__user', 'issues__issue_type',
            'issues__priority', 'issues__status', 'issues__assignee'
        ),
        pk=pk
    )
    # Check membership
    if not project.members.filter(user=request.user).exists():
        messages.error(request, '你沒有權限檢視此專案')
        return redirect('projects:list')

    issues = project.issues.all()
    statuses = {s['id']: s['name'] for s in
                project.issues.values('status__id', 'status__name').distinct()}

    # Kanban data
    from issues.models import IssueStatus, IssueType, IssuePriority
    kanban_statuses = IssueStatus.objects.all()
    kanban = {}
    for s in kanban_statuses:
        kanban[s] = issues.filter(status=s)
    
    in_progress_count = issues.exclude(status__is_closed=True).count()
    done_count = issues.filter(status__is_closed=True).count()

    return render(request, 'projects/detail.html', {
        'project': project,
        'issues': issues,
        'kanban': kanban,
        'issue_types': IssueType.objects.all(),
        'priorities': IssuePriority.objects.all(),
        'in_progress_count': in_progress_count,
        'done_count': done_count,
    })


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, '專案更新成功！')
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/form.html', {
        'form': form, 'title': '編輯專案', 'project': project
    })


@login_required
def project_members(request, pk):
    project = get_object_or_404(Project, pk=pk)
    members = project.members.select_related('user').all()

    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.save()
            messages.success(request, '成員已加入！')
            return redirect('projects:members', pk=project.pk)
    else:
        form = AddMemberForm()
        form.fields['user'].queryset = form.fields['user'].queryset.exclude(
            id__in=members.values_list('user_id', flat=True)
        )

    return render(request, 'projects/members.html', {
        'project': project,
        'members': members,
        'form': form,
    })


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, '專案已刪除')
        return redirect('projects:list')
    return render(request, 'projects/confirm_delete.html', {'project': project})
