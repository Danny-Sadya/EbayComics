from django.contrib import admin
from django.urls import path, include
from .views import dashboard_control, delete_snipe, edit_snipe, create_snipe

urlpatterns = [
    path('', dashboard_control, name='dashboard-control'),
    path('create', create_snipe, name='snipe-create'),
    path('delete/<int:pk>', delete_snipe, name='snipe-delete'),
    path('edit/<int:pk>', edit_snipe, name='snipe-edit'),
    path('', include('django.contrib.auth.urls')),
    # path('update/', update_grades, name='update-grades'),
]