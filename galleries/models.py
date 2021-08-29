from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Gallerie(models.Model):
    title           = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(blank=True,null=True)
    description     = models.CharField(max_length=300,blank=True)
    image           = models.ImageField(upload_to='image')
    timestamp       = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True,auto_now_add=False)

    class Meta:
        ordering = ["-timestamp","-updated"]

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("Gallerie-detail",kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Gallerie, self).save(*args, **kwargs)
