from datetime import date, datetime

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Article, Category
import requests
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import RegisterForm


@login_required
def home(request):
    articles = Article.objects.all()

    return render(request, "news/home.html", {
        "articles": articles
    })


@login_required
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)

    return render(request, "news/article.html", {
        "article": article
    })


@login_required
def category(request, id):
    category = get_object_or_404(Category, id=id)
    articles = Article.objects.filter(category=category)

    return render(request, "news/category.html", {
        "category": category,
        "articles": articles
    })


@login_required
def search(request):
    query = request.GET.get("q")
    articles = []

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        )

    return render(request, "news/search.html", {
        "query": query,
        "articles": articles
    })


@login_required
def current_affairs(request):
    articles = Article.objects.all()

    return render(request, "news/current_affairs.html", {
        "articles": articles
    })


@login_required
def live_news(request):

    API_KEY = "384d836eb5864d6885288597a945b7b0"

    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=20&apiKey={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except requests.exceptions.RequestException:
        data = {}

    articles = []

    if data.get("status") == "ok":
        for article in data.get("articles", []):

            if not article.get("description"):
                article["description"] = "No description available."

            if not article.get("urlToImage"):
                article["urlToImage"] = "https://placehold.co/600x400?text=No+Image"

            articles.append(article)

    return render(request, "news/live_news.html", {
        "articles": articles
    })


@login_required
def weather(request):

    API_KEY = "7e2b6fd60c96c84a25a8c7a9d289d005"

    city = request.GET.get("city", "Chennai").strip()
    if not city:
        city = "Chennai"

    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    weather_data = {}
    forecast = []
    error = None

    try:
        current_response = requests.get(current_url, timeout=10)
        forecast_response = requests.get(forecast_url, timeout=10)

        if current_response.status_code == 200:
            current_data = current_response.json()
            weather_data = {
                "city": current_data.get("name", city),
                "country": current_data.get("sys", {}).get("country", ""),
                "temp": round(current_data["main"]["temp"]),
                "feels_like": round(current_data["main"]["feels_like"]),
                "humidity": current_data["main"]["humidity"],
                "pressure": current_data["main"]["pressure"],
                "wind": current_data["wind"]["speed"],
                "visibility": round(current_data.get("visibility", 0) / 1000, 1),
                "description": current_data["weather"][0]["description"].title(),
                "icon": current_data["weather"][0]["icon"],
            }
        elif current_response.status_code == 404:
            error = f'City "{city}" not found. Please check the spelling and try again.'
        else:
            error = "Unable to fetch weather data. Please try again later."

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            seen_dates = set()
            for item in forecast_data["list"]:
                item_date = item["dt_txt"].split(" ")[0]
                if item_date not in seen_dates:
                    seen_dates.add(item_date)
                    dt = datetime.strptime(item_date, "%Y-%m-%d")
                    forecast.append({
                        "date": item_date,
                        "day": dt.strftime("%a"),
                        "full_day": dt.strftime("%A"),
                        "temp": round(item["main"]["temp"]),
                        "temp_min": round(item["main"]["temp_min"]),
                        "temp_max": round(item["main"]["temp_max"]),
                        "icon": item["weather"][0]["icon"],
                        "description": item["weather"][0]["description"].title(),
                        "humidity": item["main"]["humidity"],
                    })
            forecast = forecast[:5]

    except requests.exceptions.RequestException:
        error = "Network error. Please check your connection and try again."

    return render(request, "news/weather.html", {
        "weather": weather_data,
        "forecast": forecast,
        "city_input": city,
        "error": error,
    })


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(request, "news/register.html", {
        "form": form
    })


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("home")

    return render(request, "news/login.html")


@login_required
def profile(request):

    return render(request, "news/profile.html")


def user_logout(request):

    logout(request)

    return redirect("login")