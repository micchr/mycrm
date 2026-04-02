from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Opportunity, Task, Client
from datetime import date


@receiver(pre_save, sender=Opportunity)
def detect_stage_change(sender, instance, **kwargs):
    """
    Ce signal détecte si le statut de l'opportunité a changé.
    On stocke l'ancien statut dans l'objet pour comparaison dans post_save.
    """
    if instance.pk:
        old = Opportunity.objects.get(pk=instance.pk)
        instance._old_stage = old.stage
    else:
        instance._old_stage = None


@receiver(post_save, sender=Opportunity)
def workflow_on_stage_change(sender, instance, created, **kwargs):
    """
    Workflow automatique selon le changement de statut
    """

    # Ne s'applique qu'en modification
    if created:
        return  

    old_stage = instance._old_stage
    new_stage = instance.stage

    # ✅ Workflow 1 : Opportunité gagnée
    if old_stage != "won" and new_stage == "won":
        # 1. Créer une tâche d'onboarding
        Task.objects.create(
            opportunity=instance,
            title="Onboarding du client",
            due_date=date.today(),
            done=False
        )

        # 2. Marquer le client comme actif
        client = instance.client
        client.is_active = True  # À ajouter dans ton modèle Client
        client.save()

        # 3. Ajouter une note automatique (si tu veux ajouter un modèle Note)
        print(f"Workflow: Opportunité {instance.title} gagnée → onboarding créé.")


    # ✅ Workflow 2 : Opportunité perdue
    if old_stage != "lost" and new_stage == "lost":
        # Créer une tâche de feedback
        Task.objects.create(
            opportunity=instance,
            title="Appeler le client pour comprendre la perte",
            due_date=date.today(),
            done=False
        )

        print(f"Workflow: Opportunité {instance.title} perdue → tâche feedback créée.")