from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^category/(?P<category_name>[a-zA-Z]+)$", views.index, name="index"),
    re_path(r"^login/$", views.login_view, name="login"),
    re_path(r"^signup/$", views.signup, name='signup'),
    re_path(r"^logout/$", views.logout_view, name='logout'),
    re_path(r"^product/(?P<product_id>[a-z0-9]+)$", views.product_view, name='product_detail'),
    re_path(r"^product/add/category$", views.select_category, name='select_category'),
    re_path(r"^product/add/(?P<category_name>[a-zA-Z]+)$", views.product_creation, name='product_creation'),
    re_path(r"^profile/(?P<user_id>[0-9]+)$", views.profile, name='profile'),
    re_path(r"^profile/edit/(?P<user_id>[0-9]+)$", views.edit_profile, name='edit_profile'),
    re_path(r"^profile/edit$", views.edit_profile_post, name='edit_profile'),
    re_path(r"^admin-page/$", views.admin_page, name='admin_page'),
    re_path(r"^delete-user/(?P<user_id>[0-9]+)$", views.delete_user, name='delete_user'),
]
