from django.urls import path
from .views import (
    feed_view,
    create_post_view,
    toggle_like,
    add_comment,
    delete_post_ajax,
    view_all_comments,
    delete_comment,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('feed/', feed_view, name='feed'),  # 👈 THIS

    path("create/", create_post_view, name="create_post"),

    # ❤️ Like / Unlike (toggle)
    path("<int:post_id>/like/", toggle_like, name="toggle_like"),
    
    # 💬 Comments
    path("<int:post_id>/comment/", add_comment, name="add_comment"),
    path("<int:post_id>/comments/", view_all_comments, name="view_all_comments"),

    # 🗑️ Delete
    path("<int:post_id>/delete/", delete_post_ajax, name="delete_post"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

