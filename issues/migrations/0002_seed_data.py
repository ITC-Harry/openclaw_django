"""
Seed default issue types, priorities, and statuses.
"""
from django.db import migrations


def seed_data(apps, schema_editor):
    # Issue Types
    IssueType = apps.get_model('issues', 'IssueType')
    types = [
        ('任務', 'bi-card-list', '#0d6efd'),
        ('錯誤', 'bi-bug', '#dc3545'),
        ('功能', 'bi-star', '#198754'),
        ('改進', 'bi-arrow-up-circle', '#fd7e14'),
        ('史詩', 'bi-bookmark', '#6f42c1'),
    ]
    for name, icon, color in types:
        IssueType.objects.get_or_create(name=name, defaults={'icon': icon, 'color': color})

    # Priorities
    IssuePriority = apps.get_model('issues', 'IssuePriority')
    priorities = [
        ('最高', 5, '#dc3545'),
        ('高', 4, '#fd7e14'),
        ('中', 3, '#ffc107'),
        ('低', 2, '#0d6efd'),
        ('最低', 1, '#6c757d'),
    ]
    for name, level, color in priorities:
        IssuePriority.objects.get_or_create(name=name, defaults={'level': level, 'color': color})

    # Statuses
    IssueStatus = apps.get_model('issues', 'IssueStatus')
    statuses = [
        ('待辦', True, False, 1, '#6c757d'),
        ('進行中', False, False, 2, '#0d6efd'),
        ('已完成', False, True, 3, '#198754'),
        ('已取消', False, True, 4, '#dc3545'),
    ]
    for name, is_default, is_closed, order, color in statuses:
        IssueStatus.objects.get_or_create(
            name=name,
            defaults={'is_default': is_default, 'is_closed': is_closed,
                      'order': order, 'color': color}
        )


class Migration(migrations.Migration):
    dependencies = [
        ('issues', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_data),
    ]
