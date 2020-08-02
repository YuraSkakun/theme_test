from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client

from testsuite.models import Test

PK = 1


class BaseFlowTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)
        self.client = Client()
        # self.client.login(username='admin', password='admin')
        self.client.login(username='admin', password='os20sk07')

    def test_basic_flow(self):
        response = self.client.get(reverse('testsuite:start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START ▶' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testsuite:next', kwargs={'pk': PK})

        for step in range(1, questions_count + 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()
            response = self.client.post(
                path=url,
                data={
                    'answer_1': "1"
                }
            )
            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        assert 'START ANOTHER TEST ▶' in response.content.decode()

    def test_success_passed(self):
        response = self.client.get(reverse('testsuite:start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START ▶' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testsuite:next', kwargs={'pk': PK})

        variants = [{'answer_3': '1'}, {'answer_2': '1'}, {'answer_3': '1'}, {'answer_3': '1'}]

        for step, variant in enumerate(variants, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()
            response = self.client.post(
                path=url,
                data=variant
            )
            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        assert 'START ANOTHER TEST ▶' in response.content.decode()
        assert '4 of 4 (100.00%)' in response.content.decode()
        # assert '4.0' in response.content.decode()
        self.assertIn('4.0', response.content.decode())

    def test_success_failed(self):
        response = self.client.get(reverse('testsuite:start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START ▶' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testsuite:next', kwargs={'pk': PK})

        variants = [{'answer_3': '1'}, {'answer_2': '1'}, {'answer_2': '1'}, {'answer_2': '1'}]

        for step, variant in enumerate(variants, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()
            response = self.client.post(
                path=url,
                data=variant
            )
            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        assert 'START ANOTHER TEST ▶' in response.content.decode()
        assert '2 of 4 (50.00%)' in response.content.decode()
        # assert '2.8333333333333335' in response.content.decode()
        self.assertIn('2.8333333333333335', response.content.decode())
