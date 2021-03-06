# pages.urls.py

from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.aboutUs, name='aboutUs'),
    path('recruitment/', views.recruit, name='recruit'),
    path('recruitment/<msg>/', views.recruit, name='recruit'),
    path('recruit-form/', views.recruitForm, name='recruitForm'),
    path('contact-us/', views.contactUs, name='contactUs'),
    path('contact-us/<msg>/', views.contactUs, name='contactUs'),
    path('contact-form/', views.contactForm, name='contactForm'),
]
