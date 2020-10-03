from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):  # debe siempre llamarse asi
        User.objects.create_user('test', 'test@test.com', 'test1234')

    def test_profile_exists(self):  # el nombre de la funcion debe empezar siempre con test_
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)

"""Para ejecutar la prueba, python3 manage.py test registration"""
