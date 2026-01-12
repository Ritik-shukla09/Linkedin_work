

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


# register new user and auto-login
def register_view(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = RegisterForm()

    return render(request, "Accounts/register.html", {"form": form})


# login user
def login_view(request):
    if request.method == "GET" and "next" in request.GET:
        messages.info(request, "Please log in to continue")

    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect(request.GET.get("next") or "feed")

        messages.error(request, "Invalid username or password")

    return render(request, "Accounts/login.html")




from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")



from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    connections_count = (
        user.sent_requests.filter(status="accepted").count() +
        user.received_requests.filter(status="accepted").count()
    )
    followers_count = user.followers.count()
    following_count = user.following.count()

    skills_list = []
    if profile.skills:
        skills_list = [s.strip() for s in profile.skills.split(",")]

    experiences = profile.experiences.all().order_by("-start_date")
    projects = profile.projects.all().order_by("-id")
    educations = profile.educations.all().order_by("-start_year")

    return render(request, "Accounts/profile.html", {
        "profile": profile,
        "connections_count": connections_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "skills_list": skills_list,
        "experiences": experiences,
        "projects": projects,
        "educations": educations,
    })




from .forms import ProfileForm

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "Accounts/edit_profile.html", {"form": form})


from .models import Experience
from .forms import ExperienceForm
from django.shortcuts import get_object_or_404

# add experience
@login_required
def add_experience(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = profile
            exp.save()
            return redirect("profile")
    else:
        form = ExperienceForm()

    return render(request, "Accounts/experience_form.html", {
        "form": form,
        "title": "Add Experience"
    })


# edit or delete experience
@login_required
def edit_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, profile=request.user.profile)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            exp.delete()
            return redirect("profile")

        if action == "save":
            form = ExperienceForm(request.POST, instance=exp)
            if form.is_valid():
                form.save()
                return redirect("profile")

        return redirect("profile")

    form = ExperienceForm(instance=exp)
    return render(request, "Accounts/experience_form.html", {
        "form": form,
        "title": "Edit Experience"
    })



from .models import Project
from .forms import ProjectForm

# add project
@login_required
def add_project(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.profile = profile
            proj.save()
            return redirect("profile")
    else:
        form = ProjectForm()

    return render(request, "Accounts/project_form.html", {
        "form": form,
        "title": "Add Project"
    })


# edit or delete project
@login_required
def edit_project(request, pk):
    proj = get_object_or_404(Project, pk=pk, profile=request.user.profile)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            proj.delete()
            return redirect("profile")

        if action == "save":
            form = ProjectForm(request.POST, instance=proj)
            if form.is_valid():
                form.save()
                return redirect("profile")

        return redirect("profile")

    form = ProjectForm(instance=proj)
    return render(request, "Accounts/project_form.html", {
        "form": form,
        "title": "Edit Project"
    })



from .models import Education
from .forms import EducationForm

# add education
@login_required
def add_education(request):
    profile = request.user.profile

    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = profile
            edu.save()
            return redirect("profile")
    else:
        form = EducationForm()

    return render(request, "Accounts/education_form.html", {
        "form": form,
        "title": "Add Education"
    })


# edit or delete education
@login_required
def edit_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, profile=request.user.profile)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            edu.delete()
            return redirect("profile")

        if action == "save":
            form = EducationForm(request.POST, instance=edu)
            if form.is_valid():
                form.save()
                return redirect("profile")

        return redirect("profile")

    form = EducationForm(instance=edu)
    return render(request, "Accounts/education_form.html", {
        "form": form,
        "title": "Edit Education"
    })



# delete logged-in user account
@login_required
@require_POST
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("login")



from django.contrib.auth import get_user_model
from django.db.models import Q
from Posts.models import Post
from Connections.models import Follow, ConnectionRequest

User = get_user_model()

# view other user's profile
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    followers_count = Follow.objects.filter(following=user).count()
    connections_count = ConnectionRequest.objects.filter(
        Q(sender=user, status="accepted") |
        Q(receiver=user, status="accepted")
    ).count()

    skills_list = []
    if user.profile.skills:
        skills_list = [s.strip() for s in user.profile.skills.split(",")]

    posts = Post.objects.filter(author=user).order_by("-created_at")

    return render(request, "Accounts/view_profile.html", {
        "profile_user": user,
        "skills_list": skills_list,
        "followers_count": followers_count,
        "connections_count": connections_count,
        "posts": posts,
    })



# search user by username
@login_required
def search_user(request):
    query = request.GET.get("q", "").strip()

    if not query:
        messages.warning(request, "Enter a username to search")
        return redirect("feed")

    user = User.objects.filter(username__iexact=query).first()

    if not user:
        return render(request, "Accounts/search_profile.html", {
            "error": "User not found",
            "query": query,
        })

    posts = Post.objects.filter(author=user).order_by("-created_at")

    followers_count = Follow.objects.filter(following=user).count()
    connections_count = ConnectionRequest.objects.filter(
        Q(sender=user, status="accepted") |
        Q(receiver=user, status="accepted")
    ).count()

    skills_list = []
    if user.profile.skills:
        skills_list = [s.strip() for s in user.profile.skills.split(",")]

    return render(request, "Accounts/search_profile.html", {
        "profile_user": user,
        "skills_list": skills_list,
        "followers_count": followers_count,
        "connections_count": connections_count,
        "posts": posts,
        "query": query,
    })



# logout user and show home page
def home(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "home.html")
