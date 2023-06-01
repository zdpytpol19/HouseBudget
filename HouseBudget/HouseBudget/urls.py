"""HouseBudget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from Budget.views import main_page,IncomeAddView,OutcomeAddView,IncomeListView,OutcomeListView,IncomeDeletelView

from django.contrib.auth import views as auth_views
from Budget import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("main_page", main_page),
    path('', user_views.home, name='home'),
    path("add_income_cbv", IncomeAddView.as_view(), name="add_income_cbv"),
    path("add_outcome_cbv/", OutcomeAddView.as_view(), name="add_outcome_cbv"),
    path('register/', user_views.register, name='register'),
    path("income_list", IncomeListView.as_view(), name="income_list"),
    path("outcome_list", OutcomeListView.as_view(), name="outcome_list"),
    path("income_delete/<int:id>", IncomeDeletelView.as_view(), name="income_delete"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),


]
