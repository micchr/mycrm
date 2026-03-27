"""
URL configuration for mycrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from crm import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('clients/', views.clients_list),
    path('clients/add/', views.client_create),
    path("contacts/", views.contacts_list),
    path("contacts/add/", views.contact_create),
    path("opportunities/", views.opportunities_list),
    path("opportunities/add/", views.opportunity_create),
    path("tasks/", views.tasks_list),
    path("tasks/add/", views.task_create),
    path("clients/<int:id>/edit/", views.client_edit),
    path("clients/<int:id>/delete/", views.client_delete),
    path("contacts/<int:id>/edit/", views.contact_edit),
    path("contacts/<int:id>/delete/", views.contact_delete),
    path("opportunities/<int:id>/edit/", views.opportunity_edit),
    path("opportunities/<int:id>/delete/", views.opportunity_delete),
    path("tasks/<int:id>/edit/", views.task_edit),
    path("tasks/<int:id>/delete/", views.task_delete),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
