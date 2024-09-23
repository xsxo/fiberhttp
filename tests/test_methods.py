import unittest
from fiberhttp import get, post, delete, put

class TestHttpClientRequests(unittest.TestCase):

    def test_get_request(self):
        response = get('https://httpbin.org/get')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['url'], 'https://httpbin.org/get')

    def test_post_request(self):
        response = post('https://httpbin.org/post', data={'usrname':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'usrname=ndoshy')

    def test_put_request(self):
        response = put('https://httpbin.org/put', data={'usrname':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'usrname=ndoshy')

    def test_delete_request(self):
        response = delete('https://httpbin.org/delete')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['url'], 'https://httpbin.org/delete')

    # def test_patch_request(self):
    #     response = patch('https://httpbin.org/patch', data={'usrname':'ndoshy'})
    #     self.assertEqual(response.status_code(), 200)
    #     self.assertEqual(response.json()['data'], 'usrname=ndoshy')

if __name__ == '__main__':
    test = unittest.main()


