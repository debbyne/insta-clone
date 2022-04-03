from django.db import models
from email.mime import image
from django.contrib.auth.models import User
from unicodedata import name
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
     name=models.CharField(max_length=50, blank=True)
     bio=models.TextField(max_length=400, default="My Bio",blank=True)
     profile_photo=models.ImageField(upload_to = 'photos/',default="",null=True)
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
     location = models.CharField(max_length=50, blank=True)
     followers = models.ManyToManyField('Profile', related_name = 'followers_profile', blank =True)
     following = models.ManyToManyField('Profile', related_name='following_profile', blank =True)


     def __str__(self):
        return f'{self.user.username} Profile'

     @receiver(post_save, sender=User)
     def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

     @receiver(post_save, sender=User)
     def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

     def save_profile(self):
        self.user

     def delete_profile(self):
        self.delete()

     def get_number_of_followers(self):
        if self.followers.count():
         return self.followers.count()
        else:
         return 0

     def get_number_of_following(self):
        if self.following.count():
         return self.following.count()
        else:
         return 0
     def __str__(self):
        return self.user.username


     @classmethod
     def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

     def __str__(self):
        return f'{self.user.username} Profile'


class Post(models.Model):
    image = models.ImageField(upload_to = 'photos/',default="",null=True)
    name = models.CharField(max_length=50,null=True)
    caption = models.CharField(max_length=100,null=True)
    # image = CloudinaryField('image')
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', null=True)
    time_created=models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

    @property
    def get_all_comments(self):
        return self.comments.all()

    def save_image(self):
        self.save()

    def total_likes(self):
        return self.likes.count()
    
    def delete_image(self):
        self.delete()

    def __str__(self):
        return f'{self.user.username} Post'

    @classmethod
    def update_image(cls ,id ,image):
        return cls.objects.filter(id = id).update(image = image)

class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    time_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f'{self.user.name} Post'

class Follow(models.Model):
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'{self.follower} Follow' 

 