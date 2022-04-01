from django.db import models
from email.mime import image
from unicodedata import category, name
from django.db import models
# Create your models here.
class Images(models.Model):
    image = models.ImageField(upload_to = 'photos/',default="",null=True)
    name = models.CharField(max_length=50,null=True)
    caption = models.CharField(max_length=100,null=True)
    # image = CloudinaryField('image')
    # location = models.ForeignKey(Location,on_delete=models.RESTRICT,)
    # category = models.ForeignKey(Category, on_delete=models.RESTRICT,)
