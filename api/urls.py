from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^login/$", views.login_view, name="login"),
    re_path(r"^signup/$", views.signup, name='signup'),
    re_path(r"^logout/$", views.logout_view, name='logout'),
    # re_path(r"^product/<str:product_id>$", views.product_view, name='product_detail'),
    re_path(r"^product/(?P<product_id>[a-z0-9]+)$", views.product_view, name='product_detail'),

]
