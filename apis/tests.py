import json
from os.path import join
from http import HTTPStatus

from django.conf import settings
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from rest_framework.test import force_authenticate, APIClient

from apis.views import TaskTrackViewSet
from apis import serializers
from taskTracks.models import TaskTrack


class DogViewSetTest(TestCase):
    test_fixtures = ['tasks']
    test_fixtures_list = []
    path_to_fixtures = join(str(settings.BASE_DIR), 'taskTracks/fixtures/')
    print(path_to_fixtures)
    for test_fixture in test_fixtures:
        test_fixtures_list.append(path_to_fixtures + '{}.json'.format(test_fixture))
    fixtures = test_fixtures_list
    print(test_fixtures_list)

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='odmen',
            password='odmenodmen',
            email='odmen@odmen.com'
        )

    ### Test for GET ###
    def test_viewset(self):
        request = self.factory.get('apis/v1/tasks/')
        force_authenticate(request, user=self.user)
        response = TaskTrackViewSet.as_view({'get': 'list'})(request)
        # Check if the first dog's name is Balto, like it is in the fixtures:
        tasks = TaskTrack.objects.all()
        serializer = serializers.ListTaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        # self.assertEqual(response.data['results'][0]['name'], 'Balto')
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)

    ### Test for CREATE/POST ###
    def test_task_create(self):
        data = json.dumps({
            "name": "Wishbone",
            "age": 2
        })
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('apis/v1/tasks/', data=data, content_type='application/json')
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        # Check to see if Wishbone was created
        self.assertEqual(response.data['results']['name'], 'Wishbone')
