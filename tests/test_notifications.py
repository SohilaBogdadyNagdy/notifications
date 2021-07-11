from app import app
from base64 import b64encode
import unittest


class ApiClient:
    """Performs API requests."""

    def __init__(self, app):
        self.client = app.test_client()

    def get(self, url, **kwargs):
        """Sends GET request and returns the response."""
        return self.client.get(url, headers=self.request_headers(), **kwargs)
    
    def post(self, url, data, **kwargs):
        """Sends POST request and returns the response."""
        return self.client.post(url, headers=self.request_headers(), data=data, **kwargs)


    def request_headers(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('user', 'secret')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }


class TestIntegrations(unittest.TestCase):

    def setUp(self):
        self.app = ApiClient(app)

    def test_list_notification(self):
        response = self.app.get('/notifications')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_post_notification(self):
        response = self.app.post('/notifications', {
            'message': 'New Promo code',
            'type': 'APP_PUSH'
        })
        self.assertEqual(response.status_code, 201)

    def test_post_invalid_data_notification(self):
        response = self.app.post('/notifications', {
            'message': 'New Promo code',
            'type': 'NOT_VALID'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_post_empty_notification(self):
        response = self.app.post('/notifications', {})
        self.assertEqual(response.status_code, 400)
    
    def test_get_one_notification(self):
        response = self.app.get('/notifications/384')
        self.assertEqual(response.status_code, 400)

    def test_send_notification_invalid_data(self):
            response = self.app.post('/notifications/send/384', {'userIds': []})
            self.assertEqual(response.status_code, 400)

#if __name__ == '__main__':
#    unittest.main()
