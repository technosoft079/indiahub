from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class News(models.Model):

    title = models.CharField(max_length=200)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='news_images/')

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    likes = models.ManyToManyField(User, related_name='news_like', blank=True)

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):

    news = models.ForeignKey(News, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username