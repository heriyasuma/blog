from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#from Posts.models import Post
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.
class CategorieManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type    = ContentType.objects.get_for_model(instance.__class__)
        obj_id  = instance.id
        qs = super(CategorieManager,self).filter(content_type=content_type,object_id=obj_id)
        return qs

class Categorie(models.Model):
    title           = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(blank=True)
    description     = models.CharField(max_length=300,blank=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True,auto_now_add=False)

    objects = CategorieManager()

    class Meta:
        ordering = ["-timestamp","-updated"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categorie-detail",kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Categorie, self).save(*args, **kwargs)

    @property
    def categories(self):
        instance = self
        qs = Categories.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
