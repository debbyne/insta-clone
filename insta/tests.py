from django.test import TestCase
from .models import Post

# Create your tests here.
class PostTestClass(TestCase):
    def setUp(self):
       pass
    def test_instance(self):
        self.assertTrue(isinstance(self.test_image,Post))
     
    def test_save_image(self):
        self.image.save_image()
        self.assertTrue(len(Post.objects.all()) == 1)
    def test_delete_image(self):
        self.test_image.delete_image()
        image = Post.objects.all()
        self.assertTrue(len(Post.objects.all()) ==1)