from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self) -> str:
        return "{}".format(self.caption)


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self) -> str:
        return self.full_name


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=255)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(
        default="", blank=True, null=False, unique=True, db_index=True
    )
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    post_tags = models.ManyToManyField(Tag, related_name="tags")

    def __str__(self) -> str:
        return "{} ({})".format(self.title, self.date)

    def get_absolute_url(self):
        return reverse("post-detail-page", args=[self.slug])


class Comment(models.Model):
    username = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
