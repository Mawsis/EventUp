from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic = models.ImageField(upload_to='static/images/',blank=True,null=True)
    description = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE,related_name="events")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="events")
    place = models.CharField(max_length=100) 
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    finish_date = models.DateField(auto_now=False, auto_now_add=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='static/images/',blank=True,null=True)
    public = models.BooleanField(default=True)
    link = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,related_name="comments")
    commented = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="comments")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.commenter} commented "{self.content}" about {self.commented}'
    

class Watchlist(models.Model):
    watchlister = models.ForeignKey(User,  on_delete=models.CASCADE,related_name="watchlists")
    watchlisted = models.ForeignKey(Event, on_delete=models.CASCADE,related_name="watchlists")

    def __str__(self) -> str:
        return f'{self.watchlister} watchlisted {self.watchlisted}'

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="subscriptions")
    club = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="subscriptions")

    def __str__(self) -> str:
        return f'{self.user} is subscribed to {self.club}'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts") 
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="posts")
    content = models.TextField()
    url = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.user}'s post to {self.event}" 