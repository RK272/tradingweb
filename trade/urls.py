from . import views
from django.urls import path





urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('prediction/', views.prediction, name="prediction"),
    path('training', views.training, name="training"),

    #path('registration', views.registration, name="registration"),
    #path('login', views.login, name="login"),
    path('cad', views.candlestick_chart_view, name="cad"),
    path('tab', views.tab, name="tab"),



    path('updatedb', views.updatedb, name="updatedb")]