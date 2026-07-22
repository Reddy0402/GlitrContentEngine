from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_job, name="generate-job"),
    path("jobs/<int:job_id>/", views.job_detail, name="job-detail"),
    path("health/", views.health_check, name="health-check"),
]