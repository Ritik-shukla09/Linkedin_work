from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

from Connections.models import Follow, ConnectionRequest

from .models import Post, Like, Comment
from .forms import PostForm



# FEED VIEW 

from django.views.decorators.cache import never_cache
from Posts.models import News

@never_cache
@login_required

def feed_view(request):

    posts = (
        Post.objects
        .select_related("author")
        .prefetch_related("likes", "comments__replies")
        .order_by("-created_at")
    )
    user = request.user
    profile = user.profile

    connections_count = (
        user.sent_requests.filter(status="accepted").count() +
        user.received_requests.filter(status="accepted").count()
    )

    followers_count = user.followers.count()
    following_count = user.following.count()

    news = News.objects.all()[:5]

    return render(request, "Posts/feed_layout.html", {
        "posts": posts,
        "news": news,                
        "show_comment_actions": False,
        "followers_count": followers_count,
        "connections_count": connections_count,
    })





# CREATE POST

@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("feed")
    else:
        form = PostForm()

    return render(request, "Posts/create_post.html", {"form": form})

# LIKE / UNLIKE 

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()
        return JsonResponse({
            "liked": False,
            "like_count": post.like_count()
        })

    return JsonResponse({
        "liked": True,
        "like_count": post.like_count()
    })



# ADD COMMENT / REPLY

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("comment")
        parent_id = request.POST.get("parent_id")

        if text:
            Comment.objects.create(
                user=request.user,
                post=post,
                text=text,
                parent_id=parent_id if parent_id else None
            )

    return redirect("feed")



# VIEW ALL COMMENTS (FULL THREAD)

@login_required
def view_all_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    comments = (
        Comment.objects
        .filter(post=post, parent__isnull=True)
        .prefetch_related("replies")
        .order_by("created_at")
    )

    return render(request, "Posts/all_comments.html", {
    "post": post,
    "comments": comments,
    "show_comment_actions": True,  # FULL COMMENTS PAGE
})




# DELETE COMMENT 

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    comment.delete()
    return JsonResponse({"success": True})



# DELETE POST (ONLY POST AUTHOR)

@login_required
def delete_post_ajax(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        post.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)
