import unittest, sys, pika

from apis.emit_notifiaction import emit_notification

class notification_test(unittest.TestCase):
    def test_Notify(self):
        print("\nTesting notifications")
        message = 'Task Created!'
        if pika.BlockingConnection():
            res = emit_notification(message)
            self.assertEqual(res, message)
        else:
            res = emit_notification(message)
            self.assertEqual(res, 'Message not sent.')
