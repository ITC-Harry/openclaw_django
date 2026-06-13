from django.urls import path
from . import views

app_name = 'issues'
urlpatterns = [
    path('create/', views.issue_create, name='create'),
    path('<int:pk>/', views.issue_detail, name='detail'),
    path('<int:pk>/edit/', views.issue_edit, name='edit'),
    path('<int:pk>/delete/', views.issue_delete, name='delete'),
    path('<int:pk>/status/', views.issue_update_status, name='update_status'),
]
