import unittest
from fiberhttp import Client, Request

class TestHttpClientRequests(unittest.TestCase):

    def setUp(self):
        self.Client = Client()

    def tearDown(self):
        self.Client.close()

    def test_prepare(self):
        REQ = Request()

        REQ.method = 'GET'
        REQ.url = 'https://api64.ipify.org?format=json'
        REQ.data = 'username=ndoshy'
        REQ.data = {'username':'ndoshy', 'username':'ah'}
        REQ.headers = {'Accept-Language': 'en-US,en;q=0.5'}
        REQ.data = 'username=ndoshy'
        REQ.data = ''
        REQ.url = 'https://api64.ipify.org?format=json'

        REQ.json = {'username':'ndoshy'}
        REQ.method = 'POST'
        REQ.url = 'https://httpbin.org/post'

        self.Client.connect('httpbin.org')

        response = self.Client.send(REQ)
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['json']['username'], 'ndoshy')
        # self.assertIn(list(response.json().keys())[0], 'origin')

    def test_get_request(self):
        response = self.Client.get('https://httpbin.org/get')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['url'], 'https://httpbin.org/get')

    def test_post_request(self):
        response = self.Client.post('https://httpbin.org/post', json={'username':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['json']['username'], 'ndoshy')

    def test_put_request(self):
        response = self.Client.put('https://httpbin.org/put', data={'username':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'username=ndoshy')

    def test_delete_request(self):
        response = self.Client.delete('https://httpbin.org/delete')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['url'], 'https://httpbin.org/delete')

    def test_patch_request(self):
        response = self.Client.patch('https://httpbin.org/patch', data={'username':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'username=ndoshy')

if __name__ == '__main__':
    test = unittest.main()