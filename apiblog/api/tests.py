from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


from api import views
from api.models import Posts


class TestPostsList(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = views.PostsList.as_view()
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_list(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_create(self):
        self.client.login(username="test", password="test")
        params = {
            "text": "Hello?",
            "created_by": 1
            }
        response = self.client.post('/posts/', params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))


class TestPostsDetail(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = views.PostsDetail.as_view()
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.posts = Posts.objects.create(text="The Space Between Us", created_by=self.user)
        self.posts.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_retrieve(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_update(self):
        self.client.login(username="test", password="test")
        params = {
            "text": "Hello",
            }
        response = self.client.put('/posts/1/', params, format="json")
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

class TestLikesList(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = views.LikesList.as_view()
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_retrieve(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
