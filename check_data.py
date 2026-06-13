from projects.models import Project, ProjectMember
from accounts.models import User

print("=== All Users ===")
for u in User.objects.all():
    print(f"  {u.username} ({u.get_full_name()}) role={u.role}")

print("\n=== All Projects ===")
for p in Project.objects.all():
    members = list(p.members.values_list('user__username', flat=True))
    lead_name = p.lead.username if p.lead else "None"
    print(f"  {p.key}: name={p.name}, lead={lead_name}, members={members}")
