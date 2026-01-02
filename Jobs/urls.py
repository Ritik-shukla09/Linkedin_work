from django.urls import path
from . import views

urlpatterns = [
    # Job list
    path("", views.job_list, name="job_list"),

    # Job create (recruiter)
    path("create/", views.create_job, name="create_job"),

    # Job detail
    path("<int:job_id>/", views.job_detail, name="job_detail"),

    # Apply job (separate page)
    path("<int:job_id>/apply/", views.apply_job, name="apply_job"),

    # Recruiter: view applicants
    path("<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),

    # Recruiter: accept / reject
    path(
        "application/<int:app_id>/<str:action>/",
        views.handle_application,
        name="handle_application"
    ),

    # Delete job (popup + POST)
    path("delete/<int:job_id>/", views.delete_job, name="delete_job"),

    # Optional dashboard
    path("recruiter/dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
]
