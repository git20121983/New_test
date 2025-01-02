from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISCHED)

class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT ='DF','Draft'
        PUBLISCHED = 'PB', 'Published'
        
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True) # дата добавления поста
    updated = models.DateTimeField(auto_now=True) # Дата последнего изменения
    
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    objects = models.Manager()     # menedjer, по умолчанию
    published = PublishedManager() # Конкретно-прикладной менеджер
    
    """Определение порядка сортировки 
       применяемого по умолчанию возвращаться в 
       обратном хронологичном порядке
    """
       
    class Meta:
        ordering = ['-publish']
        indexes = [                           # позволяет определить в 
            models.Index(fields=['-publish']) # моделе индексы базы данных  https://docs.djangoproject.com/en/5.1/ref/models/indexes/
        ]                                     # Был добавлен индекс полю publish с дефисом '-' 
                                              # чтоб определить индекс в убывающем порядке
                                              
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])
    