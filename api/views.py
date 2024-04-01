from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
import copy

from api import mongodb


def index(request, category_key=None):
    products_collection = mongodb["products"]
    categories_collection = mongodb["categories"]
    product_query = {"isActive": True}
    if category_key is not None and category_key != "all":
        product_query["category"] = category_key
    products_cursor = products_collection.find(product_query).sort("updated_at", pymongo.DESCENDING)
    categories_cursor = categories_collection.find().sort("name")
    products = []
    categories = []
    category_name = None
    for product in products_cursor:
        products.append(product)
        product["id"] = product["_id"]
    for category in categories_cursor:
        if category["key"] == category_key:
            category_name = category["name"]
        categories.append(category)
    if not category_name:
        category_name = "All"
    number_of_products = len(products)
    return render(request, "index.html",
                  {"categories": categories, "products": products, "number_of_products": number_of_products,
                   "category_name": category_name})


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
            if category["key"] != "all":
                categories.append(category)
        return render(request, "select-category.html", {"categories": categories})


def product_creation(request, category_key="None"):
    categories_collection = mongodb["categories"]
    category1 = categories_collection.find_one({"key": category_key})
    category_name = category1["name"]
    if request.method == 'GET':
        category1.pop("_id", None)
        category1.pop("name", None)
        category1.pop("description", None)
        category1.pop("key", None)
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            categories.append(category)
        return render(request, "product-form.html",
                      {"categories": categories, "category_name": category_name, "category_key": category_key,
                       "category_fields": category1})
    elif request.method == 'POST':
        products_collection = mongodb["products"]
        product = {}
        form_data = request.POST
        form_data = form_data.dict()
        form_data.pop("csrfmiddlewaretoken", None)
        storage_info = {}
        camera_info = {}
        lesson_list = []
        for k, v in form_data.items():
            v = v.strip(" ")
            if v:
                if category_key == "phone" and "-Camera-" in k:
                    key = k.split("-Camera-")[1]
                    camera_info[key] = v
                elif category_key == "computer" and "." in k:
                    key = k.split(".")[1]
                    storage_info[key] = v
                elif category_key == "privateLesson" and "-Lessons-" in k:
                    lesson_list.append(v)
                else:
                    product[k[2:]] = v

        product["owner_id"] = request.user.id
        product["category"] = category_key
        product["created_at"] = datetime.now()
        product["updated_at"] = datetime.now()
        product["isActive"] = True if product.get("isActive", None) else False
        if storage_info:
            product["Storage"] = storage_info
        if camera_info:
            product["Camera Specifications"] = camera_info
        if lesson_list:
            product["Lessons"] = lesson_list
        products_collection.insert_one(product)
        return redirect("/")


def product_view(request, product_id):
    if request.method == 'GET':
        users_collection = mongodb["auth_user"]
        products_collection = mongodb["products"]
        categories_collection = mongodb["categories"]
        favorites_collection = mongodb["favorites"]
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        categories_cursor = categories_collection.find().sort("name")

        is_favorite = favorites_collection.find_one({"user_id": request.user.id, "product_id": product_id}) is not None

        categories = []
        for category in categories_cursor:
            categories.append(category)

        dynamic_fields = copy.deepcopy(product)
        entries_to_remove = (
            "owner_id", "price", "category", "isActive", "updated_at", "created_at", "imageLink", "description",
            "title", "key",
            "id", "_id")
        for k in entries_to_remove:
            dynamic_fields.pop(k, None)

        user_data = users_collection.find_one({"id": product.get("owner_id", None)})
        contact_data = {"Email": user_data["email"], "Full Name": user_data["first_name"] + user_data["last_name"],
                        "Phone Number": user_data.get("phone_number", "-")}
        product["id"] = product["_id"]
        return render(request, "product-detail.html",
                      {"categories": categories, "product": product, "dynamic_fields": dynamic_fields,
                       "contact_data": contact_data, "is_favorite": is_favorite})


def edit_product(request, product_id):
    products_collection = mongodb["products"]
    if request.method == 'GET':
        categories_collection = mongodb["categories"]
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            categories.append(category)
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        category = categories_collection.find_one({"key": product["category"]})
        category_name = category["name"]
        category.pop("_id", None)
        category.pop("name", None)
        category.pop("description", None)
        category_key = category.pop("key", None)

        extra_fields = {}
        for k, v in category.items():
            extra_fields[k] = {"type": v, "value": product.get(k, "")}

        product_fields = copy.deepcopy(product)
        entries_to_remove = (
            "owner_id", "price", "category", "isActive", "updated_at", "created_at", "imageLink", "description",
            "title", "key",
            "id", "_id")
        for k in entries_to_remove:
            product_fields.pop(k, None)
        for k, v in product_fields.items():
            if k not in extra_fields:
                extra_fields[k] = {"type": v, "value": product.get(k, "")}
        product["id"] = product["_id"]
        if category_key == "privateLesson":
            product["Lessons"] = product.get("Lessons", [])
        return render(request, "edit-product.html",
                      {"categories": categories, "product": product, "category_name": category_name,
                       "extra_fields": extra_fields})
    elif request.method == 'POST':
        form_data = request.POST.dict()
        print(form_data)
        form_data["p-isActive"] = True if "p-isActive" in form_data else False
        form_data.pop("csrfmiddlewaretoken", None)
        add_list = {"updated_at": datetime.now()}
        remove_list = {}
        lesson_list = []
        camera_list = {}
        for k, v in form_data.items():
            key = k[2:]
            if v != "":
                if "-Camera-" in k:
                    camera_list[k.split("-Camera-")[1]] = v
                elif "-Lessons-" in k:
                    lesson_list.append(v)
                else:
                    add_list[key] = v
            else:
                remove_list[key] = v
        if camera_list:
            add_list["Camera Specifications"] = camera_list
        else:
            remove_list["Camera Specifications"] = camera_list
        if lesson_list:
            add_list["Lessons"] = lesson_list
        else:
            remove_list["Lessons"] = lesson_list
        products_collection.update({"_id": ObjectId(product_id)}, {"$set": add_list})
        products_collection.update({"_id": ObjectId(product_id)}, {"$unset": remove_list})
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        product_storage = product.get("Storage", None)
        if type(product_storage) == dict and not product_storage:
            products_collection.find_one_and_update({"_id": ObjectId(product_id)}, {"$unset": {"Storage": 1}})

        return redirect("/product/" + product_id)


def delete_product(request, product_id):
    products_collection = mongodb["products"]
    favorites_collection = mongodb["favorites"]
    if request.method == 'POST':
        product_query = {"_id": ObjectId(product_id)}
        products_collection.delete_many(product_query)
        favorites_query = {"product_id": product_id}
        favorites_collection.delete_many(favorites_query)
        return redirect("/")


def profile(request, user_id):
    products_collection = mongodb["products"]
    users_collection = mongodb["auth_user"]
    if request.method == 'GET':
        user_data = users_collection.find_one({"id": int(user_id)})
        categories_collection = mongodb["categories"]
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            categories.append(category)
        products = []
        products_query = {"owner_id": user_id}
        if user_id != request.user.id:
            products_query["isActive"] = True
        products_cursor = products_collection.find(products_query)
        for product in products_cursor:
            product["id"] = product["_id"]
            products.append(product)
        return render(request, "profile.html",
                      {"categories": categories, "user_data": user_data, "products": products,
                       "number_of_products": len(products)})


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
    elif request.method == 'POST':
        form_data = request.POST
        form_data = form_data.dict()
        form_data.pop("csrfmiddlewaretoken", None)
        users_collection.find_one_and_update({"id": request.user.id}, {"$set": form_data})
        return redirect("/profile/" + str(request.user.id))


def admin_page(request, user_id=None):
    users_collection = mongodb["auth_user"]
    if request.method == 'GET':
        user_data = []
        user_data_cursor = users_collection.find()
        for usr in user_data_cursor:
            data = {"id": usr["id"], "email": usr["email"], "full_name": usr["first_name"] + usr["last_name"],
                    "date_joined": usr["date_joined"], "last_login": usr["last_login"]}
            user_data.append(data)
        categories_collection = mongodb["categories"]
        categories_cursor = categories_collection.find().sort("name")
        categories = []
        for category in categories_cursor:
            categories.append(category)
        return render(request, "admin-page.html",
                      {"categories": categories, "user_data": user_data})


def delete_user(request, user_id):
    users_collection = mongodb["auth_user"]
    products_collection = mongodb["products"]
    favorites_collection = mongodb["favorites"]
    if request.method == 'POST':
        user_query = {"id": int(user_id)}
        product_query = {"owner_id": int(user_id)}
        users_collection.delete_one(user_query)
        products_collection.delete_many(product_query)
        favorites_query = {"user_id": int(user_id)}
        favorites_collection.delete_many(favorites_query)
        return redirect("/admin-page/")


def change_active_state(request, action_name, product_id):
    products_collection = mongodb["products"]
    if request.method == 'POST':
        active_state = True if action_name == "activate" else False
        change_list = {"updated_at": datetime.now(), "isActive": active_state}
        product = products_collection.find_one_and_update({"_id": ObjectId(product_id)}, {"$set": change_list})
        return redirect("/profile/" + str(product["owner_id"]))


def favorite_product(request, product_id):
    favorites_collection = mongodb["favorites"]
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect("/login")
        form_data = request.POST
        favorite_query = {"user_id": request.user.id, "product_id": product_id}
        if form_data["favorite_action"] == "add":
            favorites_collection.insert_one(favorite_query)
        else:
            favorites_collection.delete_one(favorite_query)
        return redirect("/product/" + product_id)


def favorites(request):
    favorites_collection = mongodb["favorites"]
    products_collection = mongodb["products"]
    categories_collection = mongodb["categories"]
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/login")
        categories = []
        categories_cursor = categories_collection.find().sort("name")
        for category in categories_cursor:
            categories.append(category)

        favorites = []
        favorite_query = {"user_id": request.user.id}
        favorites_cursor = favorites_collection.find(favorite_query)
        for favorite in favorites_cursor:
            favorites.append(ObjectId(favorite["product_id"]))

        products = []
        products_query = {"isActive": True, "_id": {"$in": favorites}}
        products_cursor = products_collection.find(products_query)
        for product in products_cursor:
            product["id"] = product["_id"]
            products.append(product)

        number_of_products = len(products)
        return render(request, "favorites.html",
                      {"categories": categories, "products": products, "number_of_products": number_of_products})
