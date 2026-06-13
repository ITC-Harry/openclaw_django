from django.db import models
from django.conf import settings


class IssueType(models.Model):
    name = models.CharField('名稱', max_length=50)
    icon = models.CharField('圖標', max_length=20, default='bi-bug')
    color = models.CharField('顏色', max_length=7, default='#0d6efd')

    class Meta:
        verbose_name = '議題類型'
        verbose_name_plural = '議題類型'

    def __str__(self):
        return self.name


class IssuePriority(models.Model):
    name = models.CharField('名稱', max_length=50)
    level = models.IntegerField('級別', default=0)
    color = models.CharField('顏色', max_length=7, default='#6c757d')

    class Meta:
        verbose_name = '優先級'
        verbose_name_plural = '優先級'
        ordering = ['level']

    def __str__(self):
        return self.name


class IssueStatus(models.Model):
    name = models.CharField('名稱', max_length=50)
    is_default = models.BooleanField('預設狀態', default=False)
    is_closed = models.BooleanField('已關閉', default=False)
    order = models.IntegerField('排序', default=0)
    color = models.CharField('顏色', max_length=7, default='#6c757d')

    class Meta:
        verbose_name = '狀態'
        verbose_name_plural = '狀態'
        ordering = ['order']

    def __str__(self):
        return self.name


class Issue(models.Model):
    project = models.ForeignKey(
        'projects.Project', on_delete=models.CASCADE,
        related_name='issues', verbose_name='專案'
    )
    summary = models.CharField('摘要', max_length=500)
    description = models.TextField('描述', blank=True)
    issue_type = models.ForeignKey(
        IssueType, on_delete=models.PROTECT,
        related_name='issues', verbose_name='類型'
    )
    priority = models.ForeignKey(
        IssuePriority, on_delete=models.PROTECT,
        related_name='issues', verbose_name='優先級'
    )
    status = models.ForeignKey(
        IssueStatus, on_delete=models.PROTECT,
        related_name='issues', verbose_name='狀態'
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='reported_issues', verbose_name='報告人'
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_issues',
        verbose_name='負責人'
    )
    labels = models.CharField('標籤', max_length=500, blank=True,
                               help_text='逗號分隔')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '議題'
        verbose_name_plural = '議題'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.project.key}-{self.id}: {self.summary}'


class Comment(models.Model):
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE,
        related_name='comments', verbose_name='議題'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='comments', verbose_name='作者'
    )
    text = models.TextField('內容')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '評論'
        verbose_name_plural = '評論'
        ordering = ['created_at']

    def __str__(self):
        return f'@{self.author} on #{self.issue_id}'
