import random
from django.urls import reverse
from rest_framework.test import APITestCase, force_authenticate
from datetime import datetime, timedelta

from apis.tests.api_factory import TaskTrackFactory
from taskTracks.models import TaskTrack, User


class views_basic_test(APITestCase):
    
    def test_1(self):
        print("\nTesting LIST.")

        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin')
        self.client.force_authenticate(admin)

        tasks = TaskTrackFactory.create_batch(random.randint(1, 5))
        response = self.client.get(reverse('apis:tasklist-list'))

        self.assertEquals(200, response.status_code)
        self.assertEquals(len(tasks), len(response.data))

    def test_2(self):
        print("\nTesting RETRIEVE.")
  
        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin')
        self.client.force_authenticate(admin)

        task = TaskTrackFactory.create(owner=admin)
        response = self.client.get(reverse('apis:tasklist-detail', args=[task.id]))

        self.assertEquals(200, response.status_code)
        self.assertEquals(task.name, response.data['name'])
        self.assertEquals(task.description, response.data['description'])
        self.assertEquals((task.date + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%f+03:00"), response.data['date'])
        self.assertEquals(str(task.state), response.data['state'])
        self.assertEquals(str(task.priority), response.data['priority'])
        self.assertEquals(task.owner.id, response.data['owner'])

    def test_3(self):
        print("\nTesting UPDATE.")
        
        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin')
        self.client.force_authenticate(admin)

        task = TaskTrackFactory(
            name='TestingPut',
            description='Blah blah blah',
            state='to_do',
            owner=admin
        )

        payload = {
            'name':'TestingPut',
            'description': 'Blah blah blah, Updated',
            'state': 'in_pr',
        }
        
        response = self.client.put(reverse('apis:tasklist-detail', args=[task.id]), payload)
        task.refresh_from_db()

        self.assertEquals(200, response.status_code)
        self.assertEquals(response.data['description'], payload['description'])
        self.assertEquals(response.data['state'], payload['state'])

        self.assertEquals(task.description, payload['description'])
        self.assertEquals(task.state, payload['state'])

    def test_4(self):
        print("\nTesting CREATE.")

        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin')
        self.client.force_authenticate(admin)

        payload = {
            'name': 'TestingCreateTask',
            'description': 'Blah blah blah',
            'state': 'to_do',
            'priority': '1_med',
            'owner': admin.id
        }

        response = self.client.post(reverse('apis:tasklist-list'), payload)
        task = TaskTrack.objects.last() 

        self.assertEquals(201, response.status_code)
        self.assertEquals(response.data['name'], payload['name'])
        self.assertEquals(response.data['description'], payload['description'])
        self.assertEquals(response.data['state'], payload['state'])
        self.assertEquals(response.data['priority'], payload['priority'])

        self.assertEquals(task.name, payload['name'])
        self.assertEquals(task.description, payload['description'])
        self.assertEquals(task.state, payload['state'])
        self.assertEquals(task.priority, payload['priority'])
        self.assertEquals(task.owner.id, response.data['owner'])

    def test_5(self):
        print("\nTesting DESTROY.")
                
        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin')
        self.client.force_authenticate(admin)
        
        task = TaskTrackFactory.create(owner=admin)
        count = TaskTrack.objects.count()
        response = self.client.delete(reverse('apis:tasklist-detail', args=[task.id]))

        self.assertEquals(204, response.status_code)
        self.assertEquals(TaskTrack.objects.count(), count-1)


class views_user_restrictions_test(APITestCase):
    
    def test_1(self):
        print("\nTesting LIST with user restrictions.")

        user0 = User.objects.create_user('user0', 'user0@gmail.com', 'user0user0')
        user = User.objects.create_user('user', 'user@gmail.com', 'useruser')
        self.client.force_authenticate(user)

        TaskTrackFactory.create(owner=user0)
        TaskTrackFactory.create(owner=user)
        response = self.client.get(reverse('apis:tasklist-list'))

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, len(response.data))

    def test_2(self):
        print("\nTesting RETRIEVE with user restrictions.")
  
        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin')        
        user = User.objects.create_user('user', 'user@gmail.com', 'useruser')
        self.client.force_authenticate(user)

        task1 = TaskTrackFactory.create(owner=admin)
        task2 = TaskTrackFactory.create(owner=user)

        response_f = self.client.get(reverse('apis:tasklist-detail', args=[task1.id]))
        self.assertEquals(404, response_f.status_code)

        response_ok = self.client.get(reverse('apis:tasklist-detail', args=[task2.id]))
        self.assertEquals(200, response_ok.status_code)
        self.assertEquals(task2.name, response_ok.data['name'])
        self.assertEquals(task2.description, response_ok.data['description'])
        self.assertEquals((task2.date + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%f+03:00"), response_ok.data['date'])
        self.assertEquals(str(task2.state), response_ok.data['state'])
        self.assertEquals(str(task2.priority), response_ok.data['priority'])
        self.assertEquals(task2.owner.id, response_ok.data['owner'])

    def test_3(self):
        print("\nTesting UPDATE with user restrictions.")

        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin') 
        user = User.objects.create_user('user', 'user@gmail.com', 'useruser')
        self.client.force_authenticate(user)

        task1 = TaskTrackFactory.create(
            name='TestingPut',
            description='Blah blah blah',
            owner=admin
        )

        task2 = TaskTrackFactory.create(
            name='TestingPut',
            description='Blah blah blah',
            owner=user
        )

        payload1 = {
            'name': 'PuttingTest',
            'description': 'Blah blah blah, Updated',
            'state': 'complt',
        }
        payload2 = {
            'description': 'Blah blah blah, Updated',
            'state': 'in_pr',
        }
        
        response_f1 = self.client.put(reverse('apis:tasklist-detail', args=[task2.id]), payload1)
        task1.refresh_from_db()
        self.assertEquals(401, response_f1.status_code)
        self.assertEquals(response_f1.data, None)

        response_f2 = self.client.put(reverse('apis:tasklist-detail', args=[task1.id]), payload2)
        task1.refresh_from_db()
        self.assertEquals(404, response_f2.status_code)

        response_ok = self.client.put(reverse('apis:tasklist-detail', args=[task2.id]), payload2)
        task2.refresh_from_db()
        self.assertEquals(200, response_ok.status_code)
        self.assertEquals(response_ok.data['description'], payload2['description'])
        self.assertEquals(response_ok.data['state'], payload2['state'])

        self.assertEquals(task2.description, payload2['description'])
        self.assertEquals(task2.state, payload2['state'])

    def test_4(self):
        print("\nTesting CREATE with user restrictions.")
  
        user = User.objects.create_user('user', 'user@gmail.com', 'useruser')
        self.client.force_authenticate(user)

        payload = {
            'name': 'TestingCreateTask',
            'description': 'Blah blah blah',
            'state': 'to_do',
            'priority': '1_med',
            'owner': user.id
        }

        response = self.client.post(reverse('apis:tasklist-list'), payload)
        task = TaskTrack.objects.last() 

        self.assertEquals(401, response.status_code)
        self.assertEquals(response.data, None)
        self.assertEquals(task, None)

    def test_5(self):
        print("\nTesting DESTROY with user restrictions.")
        
        user = User.objects.create_user('user', 'user@gmail.com', 'useruser')
        self.client.force_authenticate(user)
        
        task = TaskTrackFactory.create(owner=user)
        count = TaskTrack.objects.count()

        response_f = self.client.delete(reverse('apis:tasklist-detail', args=[task.id]))
        self.assertEquals(401, response_f.status_code)        
        self.assertEquals(TaskTrack.objects.count(), count)
