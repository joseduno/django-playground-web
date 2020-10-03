from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Para obtimizar espacio borrando el avatar anterior cuando se actualizce
def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__username']  # para que los querysets, guarden las instancias de forma ordenada por el username


# Utilizando señales para crear automaticamente perfiles asociados a usuarios que recien se crean
@receiver(post_save, sender=User)  # ejecutara función decorada después de crear instancia del modelo definido en sender
def ensure_profile_exits(sender, instance, **kwargs):
    if kwargs.get('created', False):  # para validar si es primera vez que se crea la instancia o si solo se esta editando
        Profile.objects.get_or_create(user=instance)  # crea el perfil asociado a un usuario nuevo la primera vez
