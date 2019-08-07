## Contains the main views of the project
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

## Home Page
# @brief Home Page view of the project
# @param request
# @return Http response to show home page
def index1(request):
    return render(request,'core/home_page.html')