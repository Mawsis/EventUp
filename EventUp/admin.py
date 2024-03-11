from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Watchlist)
admin.site.register(Subscription)
admin.site.register(Post)