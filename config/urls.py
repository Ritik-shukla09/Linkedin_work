# config/urls.py
from django.contrib import admin
from django.urls import path, include
from Accounts.views import home

urlpatterns = [
    path("", home, name="home"),  
    path("admin/", admin.site.urls),
    path("accounts/", include("Accounts.urls")),
    path("posts/", include("Posts.urls")),
    path("connections/", include("Connections.urls")),
    path("jobs/", include("Jobs.urls")),
    path("messages/", include("Messages.urls")),

]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
