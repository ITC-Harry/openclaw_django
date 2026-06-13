from django.urls import path
from . import views

app_name = 'pm_admin'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Issue Types
    path('issue-types/', views.issue_type_list, name='issue_type_list'),
    path('issue-types/create/', views.issue_type_create, name='issue_type_create'),
    path('issue-types/<int:pk>/edit/', views.issue_type_edit, name='issue_type_edit'),
    path('issue-types/<int:pk>/delete/', views.issue_type_delete, name='issue_type_delete'),

    # Priorities
    path('priorities/', views.priority_list, name='priority_list'),
    path('priorities/create/', views.priority_create, name='priority_create'),
    path('priorities/<int:pk>/edit/', views.priority_edit, name='priority_edit'),
    path('priorities/<int:pk>/delete/', views.priority_delete, name='priority_delete'),

    # Statuses
    path('statuses/', views.status_list, name='status_list'),
    path('statuses/create/', views.status_create, name='status_create'),
    path('statuses/<int:pk>/edit/', views.status_edit, name='status_edit'),
    path('statuses/<int:pk>/delete/', views.status_delete, name='status_delete'),

    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/toggle-staff/', views.user_toggle_staff, name='user_toggle_staff'),
    path('users/<int:pk>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),

    # All Projects
    path('all-projects/', views.all_projects, name='all_projects'),
]
