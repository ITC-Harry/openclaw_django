from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Issue, Comment, IssueStatus
from .forms import IssueForm, CommentForm
from projects.models import Project


@login_required
def issue_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    default_status = IssueStatus.objects.filter(is_default=True).first()

    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.project = project
            issue.reporter = request.user
            if not issue.status_id:
                issue.status = default_status
            issue.save()
            messages.success(request, f'議題 {issue} 建立成功！')
            return redirect('projects:detail', pk=project.pk)
    else:
        form = IssueForm(initial={'status': default_status})
    return render(request, 'issues/form.html', {
        'form': form, 'project': project, 'title': '建立議題'
    })


@login_required
def issue_detail(request, project_pk, pk):
    project = get_object_or_404(Project, pk=project_pk)
    issue = get_object_or_404(
        Issue.objects.select_related(
            'issue_type', 'priority', 'status', 'reporter', 'assignee'
        ).prefetch_related('comments__author'),
        pk=pk, project=project
    )

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue = issue
            comment.author = request.user
            comment.save()
            messages.success(request, '評論已新增！')
            return redirect('issues:detail', project_pk=project.pk, pk=issue.pk)
    else:
        form = CommentForm()

    return render(request, 'issues/detail.html', {
        'issue': issue, 'project': project, 'form': form,
    })


@login_required
def issue_edit(request, project_pk, pk):
    project = get_object_or_404(Project, pk=project_pk)
    issue = get_object_or_404(Issue, pk=pk, project=project)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, '議題已更新！')
            return redirect('issues:detail', project_pk=project.pk, pk=issue.pk)
    else:
        form = IssueForm(instance=issue)
    return render(request, 'issues/form.html', {
        'form': form, 'project': project, 'issue': issue, 'title': '編輯議題'
    })


@login_required
def issue_delete(request, project_pk, pk):
    project = get_object_or_404(Project, pk=project_pk)
    issue = get_object_or_404(Issue, pk=pk, project=project)
    if request.method == 'POST':
        issue.delete()
        messages.success(request, '議題已刪除')
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'issues/confirm_delete.html', {
        'issue': issue, 'project': project,
    })


@login_required
def issue_update_status(request, project_pk, pk):
    """AJAX: update issue status for kanban drag-and-drop"""
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=project_pk)
        issue = get_object_or_404(Issue, pk=pk, project=project)
        status_id = request.POST.get('status_id')
        if status_id:
            new_status = get_object_or_404(IssueStatus, pk=status_id)
            issue.status = new_status
            issue.save()
            messages.success(request, f'狀態已變更為 {new_status.name}')
    return redirect('projects:detail', pk=project_pk)
