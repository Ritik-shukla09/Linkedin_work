from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Job, JobApplication
from .decorators import recruiter_required, applicant_required



# JOB LIST 
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import never_cache

@never_cache
@login_required

def job_list(request):
    jobs = Job.objects.all().order_by("-created_at")

    applied_jobs = []
    if request.user.is_authenticated and request.user.role in ["student", "professional"]:
        applied_jobs = JobApplication.objects.filter(
            applicant=request.user
        ).values_list("job_id", flat=True)

    return render(request, "Jobs/job_list.html", {
        "jobs": jobs,
        "applied_jobs": applied_jobs
    })


# JOB APPLICANTS (Recruiter only)


@never_cache
@login_required
@recruiter_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # safety: only owner recruiter can see applicants
    if job.posted_by != request.user:
        raise PermissionDenied

    applications = JobApplication.objects.filter(
        job=job
    ).select_related("applicant")

    return render(request, "Jobs/job_applicants.html", {
        "job": job,
        "applications": applications
    })


# JOB DETAIL PAGE


@never_cache
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    application = None
    if request.user.is_authenticated:
        application = JobApplication.objects.filter(
            job=job,
            applicant=request.user
        ).first()

    return render(request, "Jobs/job_detail.html", {
        "job": job,
        "application": application
    })




# CREATE JOB (Recruiter only)


@never_cache
@login_required
@recruiter_required
def create_job(request):
    if request.method == "POST":
        Job.objects.create(
            title=request.POST["title"],
            company=request.POST["company"],
            location=request.POST["location"],
            description=request.POST["description"],
            posted_by=request.user
        )
        return redirect("job_list")

    return render(request, "Jobs/create_job.html")



# APPLY JOB (Applicant only)


@never_cache
@login_required
@applicant_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    already_applied = JobApplication.objects.filter(
        job=job,
        applicant=request.user
    ).exists()

    if already_applied:
        return redirect("job_detail", job_id=job.id)

    if request.method == "POST":
        JobApplication.objects.create(
            job=job,
            applicant=request.user,
            resume=request.FILES["resume"],
            cover_letter=request.POST.get("cover_letter", "")
        )
        return redirect("job_detail", job_id=job.id)

    return render(request, "Jobs/apply_job.html", {"job": job})



# RECRUITER DASHBOARD


@never_cache
@login_required
@recruiter_required

def recruiter_dashboard(request):
    jobs = Job.objects.filter(
        posted_by=request.user
    ).prefetch_related("jobapplication_set")

    return render(request, "Jobs/recruiter_dashboard.html", {
        "jobs": jobs
    })



@never_cache
@login_required
@recruiter_required

def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.posted_by != request.user:
        return redirect("job_list")

    if request.method == "POST":
        job.delete()

    return redirect("job_list")

@never_cache
@login_required
@recruiter_required
def handle_application(request, app_id, action):
    application = get_object_or_404(JobApplication, id=app_id)

    # safety check
    if application.job.posted_by != request.user:
        raise PermissionDenied

    if action == "accept":
        application.status = "accepted"
        application.save()

    elif action == "reject":
        application.delete()

    return redirect("job_applicants", job_id=application.job.id)
