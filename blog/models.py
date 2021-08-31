from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from galleries.models import Gallerie
from django.conf import settings
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models import Q

# Create your models here.
def get_sentinel_category():
    return Categorie.objects.get_or_create(title='Uncategorized')[0]

# def get_sentinel_tag():
    # return Tag.objects.get_or_create(title='Untagged')[0]

def get_sentinel_gallerie():
    return Gallerie.objects.get_or_create(title='Deleted')[0]

class Categorie(models.Model):
    title           = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(blank=True)
    thumbnail       = models.ForeignKey(Gallerie,null=True,blank=True,on_delete=models.CASCADE)
    description     = models.CharField(max_length=300,blank=True)
    timestamp       = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True,auto_now_add=False)

    class Meta:
        ordering = ["-timestamp","-updated"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categorie-detail",kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Categorie, self).save(*args, **kwargs)

class Tag(models.Model):
    title           = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(blank=True)
    thumbnail       = models.ForeignKey(Gallerie,null=True,blank=True,on_delete=models.CASCADE)
    description     = models.CharField(max_length=300,blank=True)
    timestamp       = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True,auto_now_add=False)

    class Meta:
        ordering = ["-timestamp","-updated"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tag-detail",kwargs={"slug":self.slug})

class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
    title           = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(blank=True)
    description     = models.CharField(max_length=300)
    thumbnail       = models.ForeignKey(Gallerie,related_name='post_thumbnail_image',null=True,blank=True,on_delete=models.CASCADE)
    content         = RichTextUploadingField()
    timestamp       = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True,auto_now_add=False)
    category        = models.ForeignKey(Categorie,on_delete=models.SET(get_sentinel_category))
    tag             = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["-timestamp","-updated"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail",kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
