import unittest
from fiberhttp import get, post, delete, put, patch

class TestHttpClientRequests(unittest.TestCase):

    def test_get_request(self):
        response = get('https://httpbin.org/get?username=ndoshy')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['args']['username'], 'ndoshy')

    def test_post_request(self):
        response = post('https://httpbin.org/post', data={'username':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'username=ndoshy')

    def test_put_request(self):
        response = put('https://httpbin.org/put', data={'username':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'username=ndoshy')

    def test_delete_request(self):
        response = delete('https://httpbin.org/delete')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['url'], 'https://httpbin.org/delete')

    def test_patch_request(self):
        response = patch('https://httpbin.org/patch', json={'username':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['json']['username'], 'ndoshy')

if __name__ == '__main__':
    test = unittest.main()


