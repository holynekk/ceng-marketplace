from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from api import mongodb


def index(request, category_name=None):
    products_collection = mongodb["products"]
    categories_collection = mongodb["categories"]
    print(category_name)
    products_cursor = products_collection.find({"category": category_name} if category_name is not None and category_name != "All" else None)
    categories_cursor = categories_collection.find().sort("name")
    products = []
    categories = []
    for product in products_cursor:
        products.append(product)
        product["id"] = product["_id"]
    for category in categories_cursor:
        categories.append(category)
    number_of_products = len(products)
    return render(request, "index.html",
                  {"categories": categories, "products": products, "number_of_products": number_of_products,
                   "user": request.user})


def product_view(request, product_id):
    if request.method == 'GET':
        products_collection = mongodb["products"]
        categories_collection = mongodb["categories"]
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        categories_cursor = categories_collection.find().sort("name")

        categories = []
        for category in categories_cursor:
            categories.append(category)

        return render(request, "product-detail.html",
                      {"categories": categories, "product": product, "user": request.user})


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
        user = User.objects.create_user(form_data["email"], form_data["email"], form_data["password"])
        user.first_name = form_data["firstName"]
        user.last_name = form_data["lastName"]
        user.save()
        return redirect('/login/')


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/')
