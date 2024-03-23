from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from api import mongodb


def index(request):
    products_collection = mongodb["products"]
    categories_collection = mongodb["categories"]

    products_cursor = products_collection.find()
    categories_cursor = categories_collection.find().sort("name")

    products = []
    categories = []
    for product in products_cursor:
        products.append(product)
    for category in categories_cursor:
        categories.append(category)

    return render(request, "index.html", {"categories": categories, "user": request.user})


def login_view(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        user_credentials = request.POST
        user = authenticate(request, username=user_credentials["username"], password=user_credentials["password"])
        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login/')


def signup(request):
    if request.method == 'GET':
        return render(request, "signup.html")
    elif request.method == 'POST':
        form_data = request.POST
        print(form_data)
        user = User.objects.create_user(form_data["email"], form_data["email"], form_data["password"])
        user.first_name = form_data["firstName"]
        user.last_name = form_data["lastName"]
        user.save()
        return redirect('/login/')


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/')
