from django.db import models
from django.utils import timezone

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
    created_at = models.DateTimeField('作成日',default=timezone.now)
    category = models.ForeignKey(Category,verbose_name='カテゴリ',on_delete=models.PROTECT)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    #ブログのコメント

    name = models.CharField('コメント',max_length=30,default='名無し')
    text = models.TextField('本文')
    post = models.ForeignKey(Post,verbose_name='紐づく記事',on_delete=models.PROTECT)
    created_at = models.DateField('作成日',default=timezone.now)

    def __str__(self):
        return self.text[:10]