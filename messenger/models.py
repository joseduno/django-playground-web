from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed 

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class ThreadManager(models.Manager):
    # Para definir funciones personalizadas al modelo Thread

    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)  # self en esta clase equivale a: Thread.objects.all()
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self, user1, user2):
        thread = self.find(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread

    # Para llamar estas funciones personalizadas: Thread.objects.find(...)



class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True)
    objects = ThreadManager()

    class Meta:
        ordering = ['-updated']


# Otra forma de implementar senales!
def messages_changed(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    action = kwargs.pop("action", None)
    pk_set = kwargs.pop("pk_set", None)
    # print(instance, action, pk_set)

    false_pk_set = set()
    if action == "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                # print("Ups, ({}) no forma parte del hilo".format(msg.user))
                false_pk_set.add(msg_pk)
    
    # Borramos de pk_set los mensajes que concuerdan con los de false_pk_set
    pk_set.difference_update(false_pk_set)

    # Forzar la actualizacion haciendo save
    instance.save()

m2m_changed.connect(messages_changed, sender=Thread.messages.through)
# --------------------------------------------------------------------------