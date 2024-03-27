from django.urls import path
from api import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category_key>", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout_view, name='logout'),
    path("product/<str:product_id>", views.product_view, name='product_detail'),
    path("product/add/category", views.select_category, name='select_category'),
    path("product/add/<str:category_key>", views.product_creation, name='product_creation'),
    path("product/edit/<str:product_id>", views.edit_product, name='edit_product'),
    path("product/delete/<str:product_id>", views.delete_product, name='delete_product'),
    path("profile/<int:user_id>", views.profile, name='profile'),
    path("profile/edit/<int:user_id>", views.edit_profile, name='edit_profile'),
    path("admin-page/", views.admin_page, name='admin_page'),
    path("delete-user/<int:user_id>", views.delete_user, name='delete_user'),
    path("product/change-active-state/<str:action_name>/<str:product_id>", views.change_active_state, name='change_active_state'),
    path("product/favorite/<str:product_id>", views.favorite_product, name='favorite_product'),
    path("favorites/", views.favorites, name='favorites'),
]
