from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理員'),
        ('manager', '專案經理'),
        ('developer', '開發者'),
        ('viewer', '檢視者'),
    ]
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='developer')
    avatar = models.ImageField('頭像', upload_to='avatars/', blank=True)
    bio = models.TextField('簡介', blank=True)
    phone = models.CharField('電話', max_length=20, blank=True)

    class Meta:
        verbose_name = '用戶'
        verbose_name_plural = '用戶'

    def __str__(self):
        return self.get_full_name() or self.username
