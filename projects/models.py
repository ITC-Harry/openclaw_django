from django.db import models
from django.conf import settings


class Project(models.Model):
    TYPE_CHOICES = [
        ('software', '軟體開發'),
        ('business', '商業專案'),
        ('personal', '個人專案'),
        ('other', '其他'),
    ]

    name = models.CharField('專案名稱', max_length=200)
    key = models.CharField('專案代號', max_length=10, unique=True,
                           help_text='簡短代號，例如 PROJ')
    description = models.TextField('描述', blank=True)
    project_type = models.CharField('專案類型', max_length=20, choices=TYPE_CHOICES, default='software')
    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='led_projects', verbose_name='負責人'
    )
    is_active = models.BooleanField('啟用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '專案'
        verbose_name_plural = '專案'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.key} - {self.name}'


class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('admin', '管理員'),
        ('member', '成員'),
        ('viewer', '檢視者'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '專案成員'
        verbose_name_plural = '專案成員'
        unique_together = ['project', 'user']

    def __str__(self):
        return f'{self.user.username} @ {self.project.key} ({self.get_role_display()})'
