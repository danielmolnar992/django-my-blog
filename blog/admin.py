from django.contrib import admin

from .models import Author, Comment, Post, Tag


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "date", "author")
    list_filter = ("date", "author", "post_tags",)
    ordering = ("-date",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "post", "id", "text")


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
