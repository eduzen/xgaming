from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

class UserLogin(models.Model):
    """Users' logins, one per connection"""
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()


@receiver(user_logged_in, sender=User)
def update_user_login(sender, user, **kwargs):
    """ It captures each users' login and it creates a new userlogin """
    user.userlogin_set.create(timestamp=timezone.now())
    user.save()
