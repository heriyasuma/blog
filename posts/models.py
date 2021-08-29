from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#from ckeditor.fields import RichTextField
from django.conf import settings
from categories.models import Categorie

# Create your models here.
def get_sentinel_category():
    return Categorie.objects.get_or_create(title='Uncategorized')[0]

# def get_sentinel_tag():
    # return Tag.objects.get_or_create(title='Untagged')[0]

#def get_sentinel_gallerie():
#    return Gallerie.objects.get_or_create(title='Deleted')[0]


class PostManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type    = ContentType.objects.get_for_model(instance.__class__)
        obj_id  = instance.id
        qs = super(PostManager,self).filter(content_type=content_type,object_id=obj_id)
        return qs

class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
    title           = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(blank=True)
    description     = models.CharField(max_length=300)
#    thumbnail       = models.ForeignKey(Gallerie,related_name='post_thumbnail_image',null=True,blank=True,on_delete=models.CASCADE)
    content         = RichTextUploadingField()
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')

    timestamp       = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True,auto_now_add=False)
    category        = models.ForeignKey(Categorie,on_delete=models.SET(get_sentinel_category), null=True, blank=True)
#    tag             = models.ManyToManyField(Tag)

    objects = PostManager()

    class Meta:
        ordering = ["-timestamp","-updated"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail",kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

#    @property
#    def comments(self):
#        instance = self
#        qs = Comment.objects.filter_by_instance(instance)
#        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
