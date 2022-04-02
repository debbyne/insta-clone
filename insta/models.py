from django.db import models
from email.mime import image
from unicodedata import category, name
from django.db import models
# Create your models here.

class Profile(models.Model):
     name=models.CharField(max_length=50)
     bio=models.TextField(max_length=500,blank=True)


class Post(models.Model):
    image = models.ImageField(upload_to = 'photos/',default="",null=True)
    name = models.CharField(max_length=50,null=True)
    caption = models.CharField(max_length=100,null=True)
    # image = CloudinaryField('image')
    
    
    def save_post(self):
        self.save()

    def __str__(self):
        return self.name

    
    def delete_post(self):
        self.delete()
    @classmethod
    def update_post(cls ,id ,image):
        return cls.objects.filter(id = id).update(image = image)
    @classmethod
    def get_images(cls):
        images = cls.objects.all()
        return images