from django.test import TestCase
from people.models import DistributorPerson
from distributors.models import UserProfile


class DistributorsTest(TestCase):

    def test_DistributorPerson_creation(self):
        user = UserProfile.objects.create(username='user', password='password')
        distributor = DistributorPerson.objects.create(
            name='Jhon Doe', user=user)
        self.assertEqual(distributor.name, 'Jhon Doe')
        self.assertEqual(distributor.favorite, False)
        self.assertEqual(distributor.mentions, 0)
        self.assertEqual(distributor.user, user)
