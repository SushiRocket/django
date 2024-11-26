from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('カテゴリ',max_length=30)
    image = models.ImageField(upload_to='category_images/', blank=True,null=True)
    created_at = models.DateField('作成日',default=timezone.now)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('タイトル',max_length=255)
    image = models.ImageField(upload_to='images',verbose_name='イメージ画像',null=True, blank=True)
    text = models.TextField('本文')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='著者', null=True, blank=True)
    created_at = models.DateTimeField('作成日',default=timezone.now)
    category = models.ForeignKey(Category,verbose_name='カテゴリ',on_delete=models.PROTECT)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    #ブログのコメント

    name = models.CharField('コメント',max_length=30,default='名無し')
    text = models.TextField('本文')
    post = models.ForeignKey(Post,verbose_name='紐づく記事',on_delete=models.PROTECT)
    created_at = models.DateField('作成日',default=timezone.now)

    def __str__(self):
        return self.text[:10]


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE, verbose_name='対象の投稿')
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE, verbose_name='「いいね」したユーザー')
    created_at = models.DateTimeField('いいね日時', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_like')
        ]
        verbose_name = 'いいね'
        verbose_name_plural = 'いいね'
