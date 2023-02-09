from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    views_count = models.IntegerField()
    create_date = models.DateTimeField()


class Comment(models.Model):
    text = models.TextField()
    create_date = models.DateTimeField()
    post = models.ForeignKey(
      'Post', models.CASCADE,
      related_name='comments')

