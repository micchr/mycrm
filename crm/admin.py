from django.contrib import admin
from .models import Client, Contact, Opportunity, Task


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "phone", "owner", "created_at")
    list_filter = ("owner", "created_at")
    search_fields = ("name", "company", "email", "phone")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "email", "phone")
    search_fields = ("name", "email", "phone")
    list_filter = ("client",)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "amount", "stage", "owner", "created_at")
    list_filter = ("stage", "owner", "created_at")
    search_fields = ("title", "client__name")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "opportunity", "due_date", "done")
    list_filter = ("done", "due_date")
    search_fields = ("title",)