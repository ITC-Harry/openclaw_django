from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from issues.models import IssueType, IssuePriority, IssueStatus
from projects.models import Project
from accounts.models import User
from django import forms


# ── Forms ──────────────────────────────────────

class IssueTypeForm(forms.ModelForm):
    class Meta:
        model = IssueType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'


class IssuePriorityForm(forms.ModelForm):
    class Meta:
        model = IssuePriority
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'


class IssueStatusForm(forms.ModelForm):
    class Meta:
        model = IssueStatus
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'


# ── Views ──────────────────────────────────────

def admin_required(view):
    """Decorator that checks staff/admin status."""
    from functools import wraps
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_staff:
            messages.error(request, '你沒有管理員權限')
            return redirect('projects:list')
        return view(request, *args, **kwargs)
    return wrapper


# Dashboard
@admin_required
def dashboard(request):
    return render(request, 'pm_admin/dashboard.html', {
        'total_users': User.objects.count(),
        'total_projects': Project.objects.count(),
        'total_issue_types': IssueType.objects.count(),
        'total_priorities': IssuePriority.objects.count(),
        'total_statuses': IssueStatus.objects.count(),
    })


# ── Issue Types ────────────────────────────────

@admin_required
def issue_type_list(request):
    types = IssueType.objects.all()
    return render(request, 'pm_admin/issue_type_list.html', {'types': types})


@admin_required
def issue_type_create(request):
    if request.method == 'POST':
        form = IssueTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '類型已建立')
            return redirect('pm_admin:issue_type_list')
    else:
        form = IssueTypeForm()
    return render(request, 'pm_admin/form.html', {'form': form, 'title': '新建議題類型'})


@admin_required
def issue_type_edit(request, pk):
    obj = get_object_or_404(IssueType, pk=pk)
    if request.method == 'POST':
        form = IssueTypeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, '類型已更新')
            return redirect('pm_admin:issue_type_list')
    else:
        form = IssueTypeForm(instance=obj)
    return render(request, 'pm_admin/form.html', {'form': form, 'title': '編輯議題類型'})


@admin_required
def issue_type_delete(request, pk):
    obj = get_object_or_404(IssueType, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, '類型已刪除')
        return redirect('pm_admin:issue_type_list')
    return render(request, 'pm_admin/confirm_delete.html', {'obj': obj, 'title': '議題類型'})


# ── Issue Priorities ───────────────────────────

@admin_required
def priority_list(request):
    priorities = IssuePriority.objects.all()
    return render(request, 'pm_admin/priority_list.html', {'priorities': priorities})


@admin_required
def priority_create(request):
    if request.method == 'POST':
        form = IssuePriorityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '優先級已建立')
            return redirect('pm_admin:priority_list')
    else:
        form = IssuePriorityForm()
    return render(request, 'pm_admin/form.html', {'form': form, 'title': '新建優先級'})


@admin_required
def priority_edit(request, pk):
    obj = get_object_or_404(IssuePriority, pk=pk)
    if request.method == 'POST':
        form = IssuePriorityForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, '優先級已更新')
            return redirect('pm_admin:priority_list')
    else:
        form = IssuePriorityForm(instance=obj)
    return render(request, 'pm_admin/form.html', {'form': form, 'title': '編輯優先級'})


@admin_required
def priority_delete(request, pk):
    obj = get_object_or_404(IssuePriority, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, '優先級已刪除')
        return redirect('pm_admin:priority_list')
    return render(request, 'pm_admin/confirm_delete.html', {'obj': obj, 'title': '優先級'})


# ── Issue Statuses ─────────────────────────────

@admin_required
def status_list(request):
    statuses = IssueStatus.objects.all()
    return render(request, 'pm_admin/status_list.html', {'statuses': statuses})


@admin_required
def status_create(request):
    if request.method == 'POST':
        form = IssueStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '狀態已建立')
            return redirect('pm_admin:status_list')
    else:
        form = IssueStatusForm()
    return render(request, 'pm_admin/form.html', {'form': form, 'title': '新建狀態'})


@admin_required
def status_edit(request, pk):
    obj = get_object_or_404(IssueStatus, pk=pk)
    if request.method == 'POST':
        form = IssueStatusForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, '狀態已更新')
            return redirect('pm_admin:status_list')
    else:
        form = IssueStatusForm(instance=obj)
    return render(request, 'pm_admin/form.html', {'form': form, 'title': '編輯狀態'})


@admin_required
def status_delete(request, pk):
    obj = get_object_or_404(IssueStatus, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, '狀態已刪除')
        return redirect('pm_admin:status_list')
    return render(request, 'pm_admin/confirm_delete.html', {'obj': obj, 'title': '狀態'})


# ── Users ──────────────────────────────────────

@admin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'pm_admin/user_list.html', {'users': users})


@admin_required
def user_toggle_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_staff = not user.is_staff
    user.save()
    messages.success(request, f'{user.username} 的管理員權限已切換')
    return redirect('pm_admin:user_list')


@admin_required
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'{user.username} 的啟用狀態已切換')
    return redirect('pm_admin:user_list')


# ── All Projects ───────────────────────────────

@admin_required
def all_projects(request):
    projects = Project.objects.all().select_related('lead')
    return render(request, 'pm_admin/all_projects.html', {'projects': projects})
