from django.db import models
from django.conf import settings
# from blogs.models import Post
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type    = ContentType.objects.get_for_model(instance.__class__)
        obj_id  = instance.id
        qs = super(CommentManager,self).filter(content_type=content_type,object_id=obj_id)
        return qs

class Comment(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    content         = models.TextField(max_length=255)
    timestamp       = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True,auto_now_add=False)

    objects = CommentManager()
    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.content
