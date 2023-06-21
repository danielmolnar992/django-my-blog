from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .forms import CommentForm
from .models import Post


class StartingPage(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]  # can have multiple elements like an SQL query
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        identified_post = get_object_or_404(Post, slug=slug)
        tag_list = [tag.caption for tag in identified_post.post_tags.all()]

        return render(request, "blog/post-detail.html", {
            "post": identified_post,
            "tags": tag_list,
            "comment_form": CommentForm(),
            "comments": identified_post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, identified_post.id)
        })

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        identified_post = get_object_or_404(Post, slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = identified_post
            comment.save()

            return HttpResponseRedirect(
                reverse("post-detail-page", args=[slug])
            )

        return render(request, "blog/post-detail.html", {
            "post": identified_post,
            "tags": identified_post.post_tags.all(),
            "comment_form": comment_form,
            "comments": identified_post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, identified_post.id)
        })


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        post = get_object_or_404(Post, id=int(request.POST["post_id"][0]))
        return HttpResponseRedirect(
            reverse("post-detail-page", args=[post.slug])
        )
