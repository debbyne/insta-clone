from django.test import TestCase
from .models import Images

# Create your tests here.
class ImageTestClass(TestCase):
    def setUp(self):
       pass
    def test_instance(self):
        self.assertTrue(isinstance(self.test_image,Images))
     
    def test_save_image(self):
        self.image.save_image()
        self.assertTrue(len(Images.objects.all()) == 1)
    def test_delete_image(self):
        self.test_image.delete_image()
        image = Images.objects.all()
        self.assertTrue(len(Images.objects.all()) ==1)