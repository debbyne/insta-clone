from django.db import models
from email.mime import image
from unicodedata import category, name
from django.db import models
# Create your models here.

class Profile(models.Model):
    pass
class Images(models.Model):
    image = models.ImageField(upload_to = 'photos/',default="",null=True)
    name = models.CharField(max_length=50,null=True)
    caption = models.CharField(max_length=100,null=True)
    # image = CloudinaryField('image')
    # location = models.ForeignKey(Location,on_delete=models.RESTRICT,)
    # category = models.ForeignKey(Category, on_delete=models.RESTRICT,)

    
    def save_image(self):
        self.save()

    def __str__(self):
        return self.name

    
    def delete_image(self):
        self.delete()
    @classmethod
    def update_image(cls ,id ,image):
        return cls.objects.filter(id = id).update(image = image)
    @classmethod
    def get_images(cls):
        images = cls.objects.all()
        return images