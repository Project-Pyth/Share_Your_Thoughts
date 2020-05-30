from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
import datetime
from django.utils.timezone import now
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links With User Model
    description = models.TextField(max_length=1000, default='', blank='True')
    city = models.CharField(max_length=100, default='', blank='True')
    state = models.CharField(max_length=100, default='', blank='True')
    ph = RegexValidator(regex=r'^\+?1?\d{10,15}$', message="Enter in format +9999999999. Upto 15 digits allowed")
    phone = models.CharField(validators=[ph], max_length=17, blank=True)
    image = models.ImageField(upload_to='',blank=True, null=True)

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    blog = models.TextField()
    views=models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title

class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Blog,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)
    def __str__(self):
        return self.comment






@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

