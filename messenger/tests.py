from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Thread

# Create your tests here.
class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')

        self.thread = Thread.objects.create()

    def test_add_users_to_thread(self):
        self.thread.users.add(self.user1, self.user2)  # add sirve para agregar instancias a modelo con relacion ManyToMany
        self.assertEqual(len(self.thread.users.all()), 2)

    def test_filter_thread_by_user(self):
        self.thread.users.add(self.user1, self.user2)  # add sirve para agregar instancias a modelo con relacion ManyToMany
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])

    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)

    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Hola como estas')
        message2 = Message.objects.create(user=self.user2, content='Bien y tu?')
        self.thread.messages.add(message1, message2)
        self.assertEqual(len(self.thread.messages.all()), 2)

    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Hola como estas')
        message2 = Message.objects.create(user=self.user2, content='Bien y tu?')
        message3 = Message.objects.create(user=self.user3, content='Soy un espía')
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1,self.user2)  # La funcion 'find' es personalizada con ThreadManager (models.py)
        self.assertEqual(self.thread, thread)

    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1, self.user2) # La funcion 'find_or_create' es personalizada con ThreadManager (models.py)
        self.assertEqual(self.thread, thread)    
        thread = Thread.objects.find_or_create(self.user1, self.user3)
        self.assertIsNotNone(thread)  


"""Para ejecutar todas las prueba de la app, python3 manage.py test messenger"""
"""Para ejecutar todas las prueba de una clase, python3 manage.py test messenger.ThreadTestCase"""
"""Para ejecutar solo una prueba, python3 manage.py test messenger.ThreadTestCase.test_add_users_to_thread"""