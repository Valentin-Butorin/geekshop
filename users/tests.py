from django.test import TestCase

from users.models import User


class UserAuthTestCase(TestCase):
    success_status_code = 200
    redirect_status_code = 302

    username = 'admin'
    password = 'admin12345'
    email = 'admin@admin.ru'

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password,
            email=self.email,
        )

    def test_login_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_status_code)
        self.assertFalse(response.context['user'].is_authenticated)

        self.client.login(username=self.username, password=self.password)
        response = self.client.post('/users/login/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_status_code)
        self.assertFalse(response.context['user'].is_authenticated)

        self.client.login(username=self.username, password=self.password)
        response = self.client.post('/users/login/')
        self.assertTrue(response.context['user'].is_authenticated)

        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, self.redirect_status_code)

        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_status_code)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_anonymous_user_profile_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_status_code)
        self.assertFalse(response.context['user'].is_authenticated)

        response = self.client.get('/users/profile/', follow=True)
        self.assertEqual(response.status_code, self.success_status_code)
        self.assertEqual(response.redirect_chain[0][1], self.redirect_status_code)
        self.assertTrue(response.redirect_chain[0][0].startswith('/users/login/'))
