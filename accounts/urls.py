from django.urls import path
from . import views

urlpatterns = [

    path("", views.splash_view, name="splash"),
    path("login/", views.login_view, name="login"),

    path("register/", views.register_view, name="register"),

    path("forgot-password/", views.forgot_password, name="forgot_password"),

    path("profile/", views.profile, name="profile"),

    path("logout/", views.logout_view, name="logout"),

]