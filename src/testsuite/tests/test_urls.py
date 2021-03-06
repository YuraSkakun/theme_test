from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_public_url(self):
        urls = [
            (reverse('index'), 'Welcome to TestSuite!'),
            # ('', 'Welcome to TestSuite!'),
            # (reverse('testsuite:list'), 'Test suites'),
        ]
        for url, content in urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()

    def test_private_urls(self):
        private_urls = [
            reverse('testsuite:list'),
            reverse('testsuite:leader_board'),
        ]
        for url in private_urls:
            response = self.client.get(url)
            # '/account/login/?next=/testsuite/leader/'
            # assert response.status_code == 302
            # assert response.url.startswith(reverse('account:login'))
            self.assertRedirects(response, '{}?next={}'.format(reverse('account:login'), url))

    # def test_authorized_urls(self):
    #     # self.client.login(username='admin', password='admin')
    #     self.client.login(username='admin', password='os20sk07')
    #     auth_urls = [
    #         # (reverse('testsuite:leader_board'), 'Leader Board'),
    #         ('/testsuite/leader/', 'Leader Board')
    #     ]
    #     for url, content in auth_urls:
    #         response = self.client.get(url)
    #         print(response.status_code)
    #         assert response.status_code == 200
    #         assert content in response.content.decode()

#
# class UrlsAvailabilityTests(TestCase):
#
#     def setUp(self):
#         call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
#         self.client = Client()
#
#     def test_public_url(self):
#         urls = [
#             (reverse('index'), 'Welcome to TMB!'),
#             (reverse('test:list'), 'Test list'),
#         ]
#         for url, content in urls:
#             response = self.client.get(url)
#             self.assertEqual(response.status_code, 200)
#             if not content:
#                 self.assertContains(response.content.decode(), content)
#
#     def test_private_urls(self):
#         private_urls = [
#             reverse('leaderboard'),
#         ]
#         for url in private_urls:
#             response = self.client.get(url)
#             # '/account/login/?next=/list/'
#             assert response.status_code == 302
#             self.assertRedirects(response, '{}?next={}'.format(reverse('login'), url))
#
#     def test_authorized_urls(self):
#         self.client.login(username='admin', password='admin')
#         auth_urls = [
#             (reverse('leaderboard'), 'Leaderboard')
#         ]
#         for url, content in auth_urls:
#             response = self.client.get(url)
#             assert response.status_code == 200
#             assert content in response.content.decode()
