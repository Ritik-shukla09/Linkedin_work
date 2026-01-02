from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from .models import Post, Like, Comment
from .forms import PostForm


# =====================================================
# FEED VIEW (shows only 1–2 top-level comments)
# =====================================================
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def feed_view(request):
    posts = (
        Post.objects
        .select_related("author")
        .prefetch_related("likes", "comments__replies")
        .order_by("-created_at")
    )

    return render(request, "Posts/feed.html", {
    "posts": posts,
    "show_comment_actions": False,  # 👈 FEED PAGE
})



# =====================================================
# CREATE POST
# =====================================================
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


# =====================================================
# LIKE ↔ UNLIKE (TOGGLE, DOUBLE-CLICK FRIENDLY)
# =====================================================
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


# =====================================================
# ADD COMMENT / REPLY
# =====================================================
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


# =====================================================
# VIEW ALL COMMENTS (FULL THREAD)
# =====================================================
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
    "show_comment_actions": True,  # 👈 FULL COMMENTS PAGE
})



# =====================================================
# DELETE COMMENT (ONLY COMMENT OWNER)
# =====================================================
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    comment.delete()
    return JsonResponse({"success": True})


# =====================================================
# DELETE POST (ONLY POST AUTHOR)
# =====================================================
@login_required
def delete_post_ajax(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        post.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)
