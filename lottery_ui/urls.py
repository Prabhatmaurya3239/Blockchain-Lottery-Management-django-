"""
URL configuration for lottery_ui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from lottery_app import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget-password/', views.forget_password_view, name='Forget_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('buy/<int:lottery_id>', views.Buy, name='buy'),
    path('organizer/', views.organizer, name='organizer'),
    path('runninglotteryview/<int:lottery_id>/', views.runninglotteryview, name='runninglotteryview'),
    path('organizer/update-image/', views.update_image),
    path('organizer/update-description/', views.update_description),
    path('organizer/update-name/', views.update_name),
    
]
