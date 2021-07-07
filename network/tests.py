from django.test import TestCase
from .models import User, Post, Follow, Like

# Create your tests here.


from .models import Follow
user = User.objects.get(username='ron')
follows = Follow.objects.filter(follower=user)
print(follows)

