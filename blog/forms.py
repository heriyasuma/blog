from django.forms import ModelForm
from blog.models import Tag

class TagForm(ModelForm):
    class Meta:
        model=Tag
        fields=['title','description']
