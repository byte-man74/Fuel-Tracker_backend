from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',  include("Api.urls")),
    path('', include("Main.urls"))
]

# stage 1 
# will add name and locaation
# stage 2
 # will add other information like opening hours
 # take contact information off 