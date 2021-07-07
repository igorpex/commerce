from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

class User(AbstractUser):
    def calculate_followers(self):
        followers =  Follow.objects.filter(author=self).count()
        if followers:
            return followers
        else: 
            return 0
    def calculate_following(self):
        following = Follow.objects.filter(follower=self).count()
        if following:
            return following
        else: 
            return 0

    followers = property(calculate_followers)
    following = property(calculate_following)
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey("User", on_delete=models.PROTECT, related_name="posts_made")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def calculateLikes(self):
        likes = Like.objects.filter(post=self).count()
        if likes:
            return likes
        else: 
            return 0

    # def getMyLike(self, request):
    #     myLike = Like.objects.get(post=self, liker=request.user)
    #     if myLike:
    #         return True
    #     else: 
    #         return False
    likes = property(calculateLikes)
    # my_like = property(getMyLike)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes":self.likes,
        }
    
    def __str__(self):
        return f"{self.body[0:20]}"

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="get_followers")
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="get_authors")

    def serialize(self):
        return {
            "follower": self.follower.username,
            "author": self.author.username,
        }

    class Meta:
        unique_together = ('follower', 'author')

    def __str__(self):
        return f"{self.follower.username} follows: {self.author.username}"

class Like (models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likers")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def serialize(self):
        return {
            "liker": self.liker.username,
            "post": self.post.id,
        }

    class Meta:
        unique_together = ('liker', 'post')

    def __str__(self):
        return f"{self.liker.username} likes: {self.post.body[0:20]}"

