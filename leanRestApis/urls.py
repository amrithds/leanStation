from django.urls import include, path
from . import views

urlpatterns = [
    path('project_activity', views.downloadMasterPlan),
    path('project_activity', views.downloadMasterPlan),
]