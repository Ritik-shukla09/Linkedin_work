from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages   # 👈 THIS LINE
from django.contrib.auth.decorators import login_required



def register_view(request):
    print("REGISTER VIEW HIT:", request.path)
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = RegisterForm()

    return render(request, 'Accounts/register.html', {'form': form})
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == "GET" and "next" in request.GET:
        messages.info(request, "Please log in to search users")

    if request.user.is_authenticated:
        logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('feed')  # 🔥 cross-app redirect

        messages.error(request, "Invalid username or password")

    return render(request, 'Accounts/login.html')

@login_required
def success_view(request):
    return render(request, 'Accounts/success.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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

    # ✅ ADD THIS (FIX)
    skills_list = []
    if profile.skills:
        skills_list = [s.strip() for s in profile.skills.split(",")]

    context = {
        "profile": profile,
        "connections_count": connections_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "skills_list": skills_list,  # ✅ PASS TO TEMPLATE
    }

    return render(request, "Accounts/profile.html", context)



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,   # 🔥 THIS LINE IS REQUIRED
            instance=profile
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "Accounts/edit_profile.html", {"form": form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def delete_account(request):
    user = request.user
    logout(request)     # log out first
    user.delete()       # delete user
    return redirect("login")



# userprofileview

# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()
from django.db.models import Q

from Connections.models import Follow, ConnectionRequest
# views.py (Accounts app)

from Posts.models import Post

def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    followers_count = Follow.objects.filter(following=user).count()
    connections_count = ConnectionRequest.objects.filter(
        Q(sender=user, status="accepted") |
        Q(receiver=user, status="accepted")
    ).count()

    skills_list = []
    if hasattr(user.profile, "skills") and user.profile.skills:
        skills_list = [s.strip() for s in user.profile.skills.split(",")]

    posts = Post.objects.filter(author=user).order_by("-created_at")

    return render(request, "Accounts/view_profile.html", {
        "profile_user": user,
        "skills_list": skills_list,
        "followers_count": followers_count,
        "connections_count": connections_count,
        "posts": posts,   # 👈 ADD THIS
    })


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    """
    Logs out the user securely and redirects to login page
    """
    logout(request)
    return redirect("login")

# utils.py (or directly inside views.py)
from django.contrib.auth import logout

def force_logout_if_authenticated(request):
    if request.user.is_authenticated:
        logout(request)


from django.shortcuts import render
from django.contrib.auth import logout
def home(request):
     if request.user.is_authenticated:
        logout(request)
     return render(request, "home.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from Posts.models import Post

User = get_user_model()

@login_required
def search_user(request):
    query = request.GET.get("q", "").strip()

    user = get_object_or_404(User, username__iexact=query)

    posts = Post.objects.filter(author=user).order_by("-created_at")
    followers_count = Follow.objects.filter(following=user).count()
    connections_count = ConnectionRequest.objects.filter(
        Q(sender=user, status="accepted") |
        Q(receiver=user, status="accepted")
    ).count()

    skills_list = []
    if hasattr(user.profile, "skills") and user.profile.skills:
        skills_list = [s.strip() for s in user.profile.skills.split(",")]


    return render(
        request,
        "Accounts/search_profile.html",
        {
            "profile_user": user,
             "skills_list": skills_list,
        "followers_count": followers_count,
        "connections_count": connections_count,
            "posts": posts,
        }
    )
