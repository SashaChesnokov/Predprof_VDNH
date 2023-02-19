"""dj_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from first.views import Main_page, Info_page, Route_points_page, History_page, Route_menu_page, Route_time_page, \
    Route_interest_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main_page, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('accounts.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('info/', Info_page, name='info'),
    path('route_menu/', Route_menu_page, name='route_menu'),
    path('points_route/', Route_points_page, name='points_route'),
    path('time_route/', Route_time_page, name='time_route'),
    path('static_route/', Route_interest_page, name='static_route'),
    path('history/', History_page, name='history')

]