from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # default is the defualt pic if no picture in database
    # upload_to directory where pics are uploaded to
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self,*args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # Resize image
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)



    # Add whatever you like. City, bio

