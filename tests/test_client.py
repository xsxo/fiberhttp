import unittest
from fiberhttp import client, request

class TestHttpClientRequests(unittest.TestCase):

    def setUp(self):
        self.client = client()

    def tearDown(self):
        self.client.close()

    def test_prepare(self):
        REQ = request()

        REQ.method = 'GET'
        REQ.url = 'https://api64.ipify.org?format=json'
        REQ.data = 'username=ahmed'
        REQ.data = {'username':'ahmed', 'name':'ah'}
        REQ.headers = {'Accept-Language': 'en-US,en;q=0.5'}
        REQ.data = 'username=ahmed'
        REQ.data = ''
        REQ.url = 'https://api64.ipify.org?format=json'
        REQ.url = 'https://httpbin.org/ip'

        self.client.connect('httpbin.org')

        response = self.client.send(REQ)
        self.assertEqual(response.status_code(), 200)
        self.assertIn(list(response.json().keys())[0], 'origin')

    def test_get_request(self):
        response = self.client.get('https://httpbin.org/get')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['url'], 'https://httpbin.org/get')

    def test_post_request(self):
        response = self.client.post('https://httpbin.org/post', data={'usrname':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'usrname=ndoshy')

    def test_put_request(self):
        response = self.client.put('https://httpbin.org/put', data={'usrname':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'usrname=ndoshy')

    def test_delete_request(self):
        response = self.client.delete('https://httpbin.org/delete')
        self.assertEqual(response.status_code(), 200)
        self.assertIn(response.json()['url'], 'https://httpbin.org/delete')

    def test_patch_request(self):
        response = self.client.patch('https://httpbin.org/patch', data={'usrname':'ndoshy'})
        self.assertEqual(response.status_code(), 200)
        self.assertEqual(response.json()['data'], 'usrname=ndoshy')

if __name__ == '__main__':
    test = unittest.main()