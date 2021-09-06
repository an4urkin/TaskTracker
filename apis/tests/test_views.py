import random
from django.urls import reverse
from rest_framework.test import APITestCase
from taskTracks.models import TaskTrack
from apis.tests.factory import TaskTrackFactory


class SnippetViewsTest(APITestCase):
    def test_list_all_tasks(self):
        tasks = TaskTrackFactory.create_batch(random.randint(1, 5))

        response = self.client.get(reverse('apis:tasktracks-list'))

        print("\nTesting GET for all.")
        self.assertEquals(200, response.status_code)
        self.assertEquals(len(tasks), len(response.data))

    def test_view_specific_task(self):
        tasks = TaskTrackFactory()

        response = self.client.get(reverse('apis:tasktracks-detail', args=[tasks.id]))

        print("\nTesting GET for specific.")

        self.assertEquals(200, response.status_code)
        self.assertEquals(tasks.name, response.data['name'])
        self.assertEquals(tasks.description, response.data['description'])
        self.assertEquals(tasks.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), response.data['date'])
        self.assertEquals(str(tasks.state), response.data['state'])
        self.assertEquals(str(tasks.priority), response.data['priority'])

    def test_update_specific_task(self):
        tasks = TaskTrackFactory(
            description='Blah blah blah',
            state='to_do',
        )

        payload = {
            'description': 'Blah blah blah, Updated',
            'state': 'in_pr',
        }

        print("\nTesting PUT.")

        response = self.client.put(reverse('apis:tasktracks-detail', args=[tasks.id]), payload)
        tasks.refresh_from_db()

        self.assertEquals(200, response.status_code)
        self.assertEquals(response.data['description'], payload['description'])
        self.assertEquals(response.data['state'], payload['state'])

        self.assertEquals(tasks.description, payload['description'])
        self.assertEquals(tasks.state, payload['state'])

    def test_add_a_new_task(self):
        payload = {
            'name': 'TestingCreateTask',
            'description': 'Kekekek',
            'state': 'to_do',
            'priority': '1_med',
        }

        response = self.client.post(reverse('apis:tasktracks-list'), payload)
        task = TaskTrack.objects.first()

        print("\nTesting POST.")

        self.assertEquals(201, response.status_code)
        self.assertEquals(response.data['name'], payload['name'])
        self.assertEquals(response.data['description'], payload['description'])
        self.assertEquals(response.data['state'], payload['state'])
        self.assertEquals(response.data['priority'], payload['priority'])

        self.assertEquals(task.name, payload['name'])
        self.assertEquals(task.description, payload['description'])
        self.assertEquals(task.state, payload['state'])
        self.assertEquals(task.priority, payload['priority'])

    def test_remove_task(self):
        tasks = TaskTrackFactory()

        print("\nTesting DELETE.")

        response = self.client.delete(reverse('apis:tasktracks-detail', args=[tasks.id]))

        self.assertEquals(204, response.status_code)
        self.assertEquals(TaskTrack.objects.count(), 0)
