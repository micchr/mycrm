from django.shortcuts import render, redirect
from .models import Client, Contact, Opportunity, Task
from django.contrib.auth.decorators import login_required

from django.db.models import Sum, Count
from datetime import date

@login_required
def home(request):
    
    # Nombre de clients
    total_clients = Client.objects.filter(owner=request.user).count()

    # Opportunités ouvertes
    open_opportunities = Opportunity.objects.filter(
        owner=request.user
    ).exclude(stage="won").exclude(stage="lost").count()

    # Somme du pipeline (montant total des opportunités ouvertes)
    pipeline_value = Opportunity.objects.filter(
        owner=request.user
    ).exclude(stage="won").exclude(stage="lost").aggregate(Sum("amount"))["amount__sum"]

    if pipeline_value is None:
        pipeline_value = 0

    # Tâches en retard
    overdue_tasks = Task.objects.filter(
        opportunity__owner=request.user,
        done=False,
        due_date__lt=date.today()
    ).count()

    context = {
        "total_clients": total_clients,
        "open_opportunities": open_opportunities,
        "pipeline_value": pipeline_value,
        "overdue_tasks": overdue_tasks,
    }

    return render(request, "home.html", context)



@login_required
def clients_list(request):
    
    if request.user.is_staff:
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(owner=request.user)

    return render(request, "crm/clients_list.html", {"clients": clients})


@login_required
def client_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        company = request.POST.get("company")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        Client.objects.create(
            name=name,
            company=company,
            email=email,
            phone=phone,
            owner=request.user
        )
        return redirect("/clients/")

    return render(request, "crm/client_form.html")


@login_required
def client_edit(request, id):
    client = Client.objects.get(id=id)

    # Si l'utilisateur n'est pas admin ET n'est pas le propriétaire → interdit
    if not request.user.is_staff and client.owner != request.user:
        return redirect("/")

    if request.method == "POST":
        client.name = request.POST.get("name")
        client.company = request.POST.get("company")
        client.email = request.POST.get("email")
        client.phone = request.POST.get("phone")
        client.save()
        return redirect("/clients/")

    return render(request, "crm/client_form.html", {"client": client})


@login_required
def client_delete(request, id):
    client = Client.objects.get(id=id)

    # Si l'utilisateur n'est pas admin ET n'est pas le propriétaire → interdit
    if not request.user.is_staff and client.owner != request.user:
        return redirect("/")
    
    client.delete()
    return redirect("/clients/")


# CONTACTS
@login_required
def contacts_list(request):
    
    if request.user.is_staff:
        contacts = Contact.objects.all()
    else:
        contacts = Contact.objects.filter(client__owner=request.user)

    return render(request, "crm/contacts_list.html", {"contacts": contacts})


@login_required
def contact_create(request):
    clients = Client.objects.filter(owner=request.user)

    if request.method == "POST":
        Contact.objects.create(
            client_id=request.POST.get("client_id"),
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
        )
        return redirect("/contacts/")

    return render(request, "crm/contact_form.html", {"clients": clients})


@login_required
def contact_edit(request, id):
    
    contact = Contact.objects.get(id=id)

    if not request.user.is_staff and contact.client.owner != request.user:
        return redirect("/")

    clients = Client.objects.filter(owner=request.user)

    if request.method == "POST":
        contact.name = request.POST.get("name")
        contact.email = request.POST.get("email")
        contact.phone = request.POST.get("phone")
        contact.client_id = request.POST.get("client_id")
        contact.save()
        return redirect("/contacts/")

    return render(request, "crm/contact_form.html", {"contact": contact, "clients": clients})


@login_required
def contact_delete(request, id):
    
    contact = Contact.objects.get(id=id)

    # Permission
    if not request.user.is_staff and contact.client.owner != request.user:
        return redirect("/")

    contact.delete()
    return redirect("/contacts/")


# OPPORTUNITÉS
@login_required
def opportunities_list(request):
    
    if request.user.is_staff:
        opportunities = Opportunity.objects.all()
    else:
        opportunities = Opportunity.objects.filter(owner=request.user)

    return render(request, "crm/opportunities_list.html", {"opportunities": opportunities})


@login_required
def opportunity_create(request):
    clients = Client.objects.filter(owner=request.user)

    if request.method == "POST":
        Opportunity.objects.create(
            client_id=request.POST.get("client_id"),
            title=request.POST.get("title"),
            amount=request.POST.get("amount"),
            stage="new",
            owner=request.user
        )
        return redirect("/opportunities/")

    return render(request, "crm/opportunity_form.html", {"clients": clients})


@login_required
def opportunity_edit(request, id):
    
    opportunity = Opportunity.objects.get(id=id)

    # Permission
    if not request.user.is_staff and opportunity.owner != request.user:
        return redirect("/")

    clients = Client.objects.filter(owner=request.user)

    if request.method == "POST":
        opportunity.title = request.POST.get("title")
        opportunity.amount = request.POST.get("amount")
        opportunity.stage = request.POST.get("stage")
        opportunity.client_id = request.POST.get("client_id")
        opportunity.save()
        return redirect("/opportunities/")

    return render(request, "crm/opportunity_form.html", {
        "opportunity": opportunity,
        "clients": clients
    })


@login_required
def opportunity_delete(request, id):

    opportunity = Opportunity.objects.get(id=id)

    # Permission
    if not request.user.is_staff and opportunity.owner != request.user:
        return redirect
    opportunity.delete()
    return redirect("/opportunities/")


# TÂCHES
@login_required
def tasks_list(request):
    
    if request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter

    return render(request, "crm/tasks_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    opportunities = Opportunity.objects.filter(owner=request.user)

    if request.method == "POST":
        Task.objects.create(
            opportunity_id=request.POST.get("opportunity_id"),
            title=request.POST.get("title"),
            due_date=request.POST.get("due_date"),
            done=False
        )
        return redirect("/tasks/")

    return render(
        request,
        "crm/task_form.html",
        {"opportunities": opportunities}
    )


@login_required
def task_edit(request, id):
    
    task = Task.objects.get(id=id)

    # Permission : owner de l'opportunité associée
    if not request.user.is_staff and task.opportunity.owner != request.user:
        return redirect("/")

    opportunities = Opportunity.objects.filter(owner=request.user)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.due_date = request.POST.get("due_date")
        task.done = ("done" in request.POST)
        task.opportunity_id = request.POST.get("opportunity_id")
        task.save()
        return redirect("/tasks/")

    return render(request, "crm/task_form.html", {
        "task": task,
        "opportunities": opportunities
    })


@login_required
def task_delete(request, id):
    
    task = Task.objects.get(id=id)

    # Permission : owner de l'opportunité associée
    if not request.user.is_staff and task.opportunity.owner != request.user:
        return redirect("/")

    task.delete()
    return redirect("/tasks/")
