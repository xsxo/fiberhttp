import fiberhttp

cn = fiberhttp.Client()

response = cn.post('https://httpbin.org/post', json={'username':'ndoshy'}).json()['json']['username'] == 'ndoshy'

print(bool(response))