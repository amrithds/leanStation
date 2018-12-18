from django.urls import include, path
from . import views

urlpatterns = [
    path('downloadMasterPlan', views.downloadMasterPlan),
    path('project_activity', views.project_activity)
]