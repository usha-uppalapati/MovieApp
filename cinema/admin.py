from django.contrib import admin
from django.db import models
from .models import comment, poster, order
# Register your models here.
admin.site.register(comment)
admin.site.register(poster)
admin.site.register(order)

