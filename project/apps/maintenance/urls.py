from django.urls import path

from project.apps.maintenance import views


app_name = 'maintenance'
urlpatterns = [
    path('maintenance_scheme/', views.MaintenanceSchemeView.as_view(), name='maintenance_scheme')
]
