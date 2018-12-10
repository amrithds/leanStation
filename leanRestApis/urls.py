from django.urls import include, path
from . import views

urlpatterns = [
    path('download_master_plan', views.downloadMasterPlan),
]