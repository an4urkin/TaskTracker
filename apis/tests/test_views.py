import random
from django.urls import reverse
from rest_framework.test import APITestCase
from datetime import datetime, timedelta

from apis.tests.factory import TaskTrackFactory
from taskTracks.models import TaskTrack


class views_test(APITestCase):

    def test_list_all_tasks(self):
        print("\nTesting GET for all.")

        tasks = TaskTrackFactory.create_batch(random.randint(1, 5))
        response = self.client.get(reverse('apis:tasktracks-list'))

        self.assertEquals(200, response.status_code)
        self.assertEquals(len(tasks), len(response.data))

    def test_view_specific_task(self):
        print("\nTesting GET for specific.")
        
        tasks = TaskTrackFactory()
        response = self.client.get(reverse('apis:tasktracks-detail', args=[tasks.id]))

        self.assertEquals(200, response.status_code)
        self.assertEquals(tasks.name, response.data['name'])
        self.assertEquals(tasks.description, response.data['description'])
        self.assertEquals((tasks.date + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%f+03:00"), response.data['date'])
        self.assertEquals(str(tasks.state), response.data['state'])
        self.assertEquals(str(tasks.priority), response.data['priority'])

    def test_update_specific_task(self):
        print("\nTesting PUT.")

        tasks = TaskTrackFactory(
            description='Blah blah blah',
            state='to_do',
        )
        payload = {
            'description': 'Blah blah blah, Updated',
            'state': 'in_pr',
        }

        response = self.client.put(reverse('apis:tasktracks-detail', args=[tasks.id]), payload)
        tasks.refresh_from_db()

        self.assertEquals(200, response.status_code)
        self.assertEquals(response.data['description'], payload['description'])
        self.assertEquals(response.data['state'], payload['state'])

        self.assertEquals(tasks.description, payload['description'])
        self.assertEquals(tasks.state, payload['state'])

    def test_add_a_new_task(self):
        print("\nTesting POST.")

        payload = {
            'name': 'TestingCreateTask',
            'description': 'Kekekek',
            'state': 'to_do',
            'priority': '1_med',
        }
        response = self.client.post(reverse('apis:tasktracks-list'), payload)
        task = TaskTrack.objects.first()        

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
        print("\nTesting DELETE.")
        
        tasks = TaskTrackFactory()
        response = self.client.delete(reverse('apis:tasktracks-detail', args=[tasks.id]))

        self.assertEquals(204, response.status_code)
        self.assertEquals(TaskTrack.objects.count(), 0)
