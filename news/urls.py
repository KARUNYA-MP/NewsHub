from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path(
        "article/<int:id>/",
        views.article_detail,
        name="article_detail"
    ),

    path(
        "category/<int:id>/",
        views.category,
        name="category"
    ),

    path(
        "search/",
        views.search,
        name="search"
    ),

    path(
        "current-affairs/",
        views.current_affairs,
        name="current_affairs"
    ),

    path(
        "live-news/",
        views.live_news,
        name="live_news"
    ),

    path(
        "weather/",
        views.weather,
        name="weather"
    ),

]