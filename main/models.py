from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#from Posts.models import Post
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

from categories.models import *
from posts.models import *


#class BlogManager(models.Manager):
#    def filter_by_instance(self, instance):
#        content_type    = ContentType.objects.get_for_model(instance.__class__)
#        obj_id  = instance.id
#        qs = super(BlogManager,self).filter(content_type=content_type,object_id=obj_id)
#        return qs

class Blog(models.Model):
    title               = models.CharField(max_length=100, unique=True)
    slug                = models.SlugField(blank=True)
    description         = models.CharField(max_length=300,blank=True)
    timestamp           = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True,auto_now_add=False)

#    objects             = BlogManager()
    class Meta:
        ordering = ["-timestamp","-updated"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categorie-detail",kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    @property
    def blog_categories(self):
        instance = self
        qs = Categorie.objects.filter_by_instance(instance)
        return qs

    @property
    def blog_posts(self):
        instance = self
        qs = Post.objects.filter_by_instance(instance)
        return qs

    @property
    def blog_posts_categorie(self):
        instance = self
        qs = Post.objects.filter_by_instance(instance)
        return qs
