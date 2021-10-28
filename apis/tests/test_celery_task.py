from django.test import TransactionTestCase
from django.urls import reverse
from celery.contrib.testing.worker import start_worker
from rest_framework.test import force_authenticate

import apis
from apis.tests.api_factory import TaskTrackFactory
from taskTracks.models import User


class FooTaskTestCase(TransactionTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(apis.celery.app, perform_ping_check=False)
        cls.celery_worker.__enter__()    
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None) 
           
    def test_delete_rejected(self):
        print("\nTesting celery task to delete rejected.")

        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'adminadmin')
        self.client.force_authenticate(admin)

        task = TaskTrackFactory.create(owner=admin)
        apis.tasks.delete_rejected_tasks()
        response = self.client.get(reverse('apis:tasklist-detail', args=[task.id]))
        self.assertEquals(404, response.status_code)
        
        
