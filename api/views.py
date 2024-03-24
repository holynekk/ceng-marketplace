from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from datetime import datetime


from api import mongodb


def index(request, category_name=None):
    products_collection = mongodb["products"]
    categories_collection = mongodb["categories"]
    products_cursor = products_collection.find(
        {"category": category_name} if category_name is not None and category_name != "All" else None)
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
                  {"categories": categories, "products": products, "number_of_products": number_of_products})


def product_view(request, product_id):
    if request.method == 'GET':
        products_collection = mongodb["products"]
        categories_collection = mongodb["categories"]
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        categories_cursor = categories_collection.find().sort("name")

        categories = []
        for category in categories_cursor:
            categories.append(category)

        dynamic_fields = product
        dynamic_fields.pop("_id", None)
        dynamic_fields.pop("title", None)
        dynamic_fields.pop("description", None)
        dynamic_fields.pop("imageLink", None)

        return render(request, "product-detail.html",
                      {"categories": categories, "product": product, "dynamic_fields": dynamic_fields})


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


def select_category(request):
    if request.method == 'GET':
        categories_collection = mongodb["categories"]
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            if category["name"] != "All":
                categories.append(category)
        return render(request, "select-category.html", {"categories": categories})


def get_product_form(request, category_name):
    if request.method == 'GET':
        categories_collection = mongodb["categories"]
        category1 = categories_collection.find_one({"name": category_name})
        category1.pop("_id", None)
        category1.pop("name", None)
        category1.pop("description", None)
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            categories.append(category)
        return render(request, "product-form.html",
                      {"categories": categories, "category_name": category_name, "category_fields": category1})


def create_product(request):
    if request.method == 'POST':
        products_collection = mongodb["products"]
        product = {}
        form_data = request.POST
        form_data = form_data.dict()
        form_data.pop("csrfmiddlewaretoken", None)
        for k, v in form_data.items():
            v = v.strip(" ")
            if v:
                product[k[2:]] = v
        products_collection.insert_one(product)
        return redirect("/")


def profile(request, user_id):
    users_collection = mongodb["auth_user"]
    if request.method == 'GET':
        user_data = users_collection.find_one({"id": int(user_id)})
        categories_collection = mongodb["categories"]
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            categories.append(category)
        return render(request, "profile.html",
                      {"categories": categories, "user_data": user_data})


def edit_profile(request, user_id):
    users_collection = mongodb["auth_user"]
    if request.method == 'GET':
        user_data = users_collection.find_one({"id": int(user_id)})
        categories_collection = mongodb["categories"]
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            categories.append(category)
        return render(request, "edit-profile.html",
                      {"categories": categories, "user_data": user_data})


def edit_profile_post(request):
    users_collection = mongodb["auth_user"]
    if request.method == 'POST':
        form_data = request.POST
        form_data = form_data.dict()
        form_data.pop("csrfmiddlewaretoken", None)
        aaaaa = users_collection.find_one_and_update({"id": request.user.id}, {"$set": form_data})
        return redirect("/profile/" + str(request.user.id))
