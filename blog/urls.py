from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path("", views.StartingPage.as_view(), name="starting-page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path(
        "posts/<slug:slug>",
        views.SinglePostView.as_view(),
        name="post-detail-page"
    ),
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
