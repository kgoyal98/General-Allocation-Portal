## URL File
# Contains Information about active urls of the project
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from . import views
from allocation.models import *
from allocation.forms import *

## URL Patterns
# @brief Matches the URL and redirects accordingly
urlpatterns = [
    url(r'^allocation/', include('allocation.urls')), #< redirects to the allocation app
    url(r'^admin/', admin.site.urls), #< redirect to admin portal
    url(r'^$',views.index1,name='index1'), #< redirect to home page view
]
