import fiberhttp

cn = fiberhttp.client()

response = cn.post('https://httpbin.org/post', json={'username':'ndoshy'}).json()['json']['username'] == 'ndoshy'

print(bool(response))