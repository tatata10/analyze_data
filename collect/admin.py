from django.contrib import admin
from .models import Friend
from .models import data
from .models import standard_data

# Register your models here.


admin.site.register(Friend)

admin.site.register(data)

admin.site.register(standard_data)