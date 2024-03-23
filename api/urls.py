from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^login/$", views.login_view, name="login"),
    re_path(r"^signup/$", views.signup, name='signup'),
    re_path(r"^logout/$", views.logout_view, name='logout'),
]
