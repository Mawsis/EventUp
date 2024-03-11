from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from django.contrib.auth.models import User
from .models import *


def main(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    if request.user.is_authenticated:
        subscriptions = Subscription.objects.filter(user=request.user)
    else:
        subscriptions = []
    return render(request,"EventUp/main-page.html",{
        "events":events,
        "categories":categories,
        "subscriptions":subscriptions,
    })

def main_filter(request):
    if request.method == 'POST':
        month = request.POST["month"]
        events = Event.objects.all()
        filter_events = []
        category = Category.objects.get(name=request.POST['category'])
        for event in events:
            if category.name == "None":
                if month in str(event.start_date):
                    filter_events.append(event)
            else:
                if event.category == category and month in str(event.start_date):
                    filter_events.append(event)
        categories = Category.objects.all()
        if request.user.is_authenticated:
            subscriptions = Subscription.objects.filter(user=request.user)
        else:
            subscriptions = []
        return render(request,"EventUp/main-page.html",{
            "events":filter_events,
            "categories":categories,
            "subscriptions":subscriptions,
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("main"))
        else:
            return render(request, "EventUp/login-page.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "EventUp/login-page.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        image = request.FILES.get('image', False)
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "EventUp/signin-page.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            if image :
                profile = Profile.objects.create(user=user,profile_pic=image)
            else:
                profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "EventUp/signin-page.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("main"))
    else:
        return render(request, "EventUp/signin-page.html")
    

def show_event(request,id):
    if request.method == "GET":
        if Event.objects.filter(pk=id).exists():
            event = Event.objects.get(pk=id)
            comments = reversed(event.comments.all())
            
            return render(request,"EventUp/event-page.html",{
                "event":event,
                "comments":comments,
                "duree": (event.finish_date-event.start_date) ,
                "is_watchlisted":any(watch in request.user.watchlists.all() for watch in event.watchlists.all())

            })
        else:
            return HttpResponse("Error")
        

def create_event(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request,'EventUp/create-page.html',{
            "categories": categories
        })
    else :
        name = request.POST["name"]
        description = request.POST["description"]
        category_name = request.POST["category"]
        category = Category.objects.get(name=category_name)
        place = request.POST["place"]
        start_date = request.POST["start_date"]
        finish_date = request.POST["finish_date"]
        link = request.POST["link"]
        public = request.POST["public"]
        image = request.FILES["image"]
        organizer = request.user
        event = Event(name=name,link=link,public=public,description=description,category=category,place=place,start_date=start_date,finish_date=finish_date,organizer=organizer,image=image)
        event.save()
        return HttpResponseRedirect(reverse("main"))


def comment(request,id):
    if request.method == "POST":
        event = Event.objects.get(pk=id)
        user = request.user
        content = request.POST["content"]
        comm = Comment(commenter = user,commented = event , content=content)
        comm.save()
        return HttpResponseRedirect(reverse("event", args=[event.id]))

def club(request,name):
    if request.method == "GET":
        if User.objects.filter(username=name).exists():
            user = User.objects.get(username=name)
            if user.profile.is_verified:
                _club= Profile.objects.get(user=user)
                if request.user.is_authenticated:
                    is_subscribed = any(sub in request.user.subscriptions.all() for sub in _club.subscriptions.all())
                else:
                    is_subscribed=False
                return render(request,"EventUp/club-profile.html",{
                    "club":user,
                    "is_subscribed": is_subscribed
                })
            else:
                return HttpResponse("Error")
        else:
            return HttpResponse("Error")


def watchlist(request,id):
    if request.method == "POST":
        user = request.user
        event = Event.objects.get(pk=id)
        if Watchlist.objects.filter(watchlister=user,watchlisted=event).exists():
            watch = Watchlist.objects.get(watchlister=user,watchlisted=event)
            watch.delete()
            return HttpResponseRedirect(reverse("event", args=[id]))
        else:
            watch = Watchlist(watchlister=user,watchlisted=event)
            watch.save()
            return HttpResponseRedirect(reverse("event",args=[id]))


def unactive(request,id):
    if request.method == "POST":
        event = Event.objects.get(pk=id)
        if event.is_active :
            event.is_active = False
        else:
            event.is_active = True
        event.save()
        return HttpResponseRedirect(reverse("event",args=[id]))

def subscribe(request,id):
    if request.method =="POST":
        user = request.user
        uclub = User.objects.get(pk=id)
        club = Profile.objects.get(user=uclub)
        if Subscription.objects.filter(user=user,club=club).exists():
            sub = Subscription.objects.get(user=user,club=club)
            sub.delete()
            return HttpResponseRedirect(reverse("club", args=[club.user.username]))
        else:
            sub = Subscription(user=user,club=club)
            sub.save()
            return HttpResponseRedirect(reverse("club", args=[club.user.username]))

def profile(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request,"EventUp/profile-page.html")
        else:
            return HttpResponseRedirect(reverse("login"))


def update(request):
    if request.method == "POST":
        user = request.user
        prof = Profile.objects.get(user=user)
        user.username = request.POST['username']
        image = None
        if 'image' in request.FILES:
            image = request.FILES['image']
        description = request.POST["description"]
        
        if image:
            prof.profile_pic = image
        prof.description = description
        prof.save()
        user.save()
        return HttpResponseRedirect(reverse(club,args=[user.username]))
    else:
        return render(request,"Eventup/modify-page.html")

def team_building(request,name):
    if request.method == "GET":
        event = Event.objects.get(name=name)
        accepted =True
        if request.user.is_authenticated:
            if Post.objects.filter(event=event,user=request.user).exists():
                accepted = False
        return render(request,"EventUp/team-page.html",{
            "event":event,
            "accepted":accepted
        })
    else:
        event = Event.objects.get(name=name)
        if Post.objects.filter(user=request.user,event=event).exists():
            return HttpResponse("You already made a post on this event")
        content = request.POST["content"]
        url = request.POST["url"]
        post = Post(user=request.user,event=event,content=content,url=url)
        post.save()
        return render(request,"EventUp/team-page.html",{
            "event":event,
        })



