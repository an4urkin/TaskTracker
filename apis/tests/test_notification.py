import unittest, sys, pika

from apis.emit_notification import emit_notification

class notification_test(unittest.TestCase):

    def test_Notify(self):
        print("\nTesting notifications")
        message = 'Message sent!'

        if pika.BlockingConnection():
            res = emit_notification(message)
            self.assertEqual(res, message)

        else:
            res = emit_notification(message)
            self.assertEqual(res, 'Message not sent.')
