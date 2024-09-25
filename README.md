# FiberHTTP [![Supported Versions](https://img.shields.io/pypi/pyversions/fiberhttp.svg)](https://pypi.org/project/fiberhttp)

`FiberHTTP` High Performance HTTP Requests Library<br/>

![GIF](media/1725894429188248.gif)

The [benchmarks](https://github.com/xsxo/fiberhttp/tree/main/benchmarks) folder contains comparisons between `Fiberhttp` and other well-known libraries such as `requests`, `httpx`, `http.client`, and others. You will notice that `Fiberhttp` outperforms them every time<br/>


## Fiberhttp might not for you

Fiberhttp is designed to provide high performance but lacks many features like:

**missing Features**:
- No support for SOCKS proxies
- No support for streaming requests
- No Support redirects requests

If these features are important to you, and you value compatibility and functionality over performance, then the requests library might be a better choice for you.

## Features:
- Keep-alive (socket connection)
- Upload - download files
- Build bytes request before send the request
- Create socket connection with server before send the request
- High-performance SSL/TLS handshake, verify
- Reading responses in various formats such as JSON, headers, and cookies

## How to use
install Fiberhttp (supported all os systems)
```bash
pip install fiberhttp
```

`with client session`
```python3
import fiberhttp

# create client session with timeout
# ! timeout not requierd
cn = fiberhttp.client(timeout=10)

# send get request
res = cn.get('https://httpbin.org/ip')

status_code = res.status_code()
body = res.text()
headers = res.headers()['Date']
json = res.json()['origin']
```

`without client session`
```python3
import fiberhttp

# send request without create client
response = fiberhttp.get('https://httpbin.org/ip')
```

`with proxies`
```python3
import fiberhttp

# create client proxy
cn = fiberhttp.client_proxy('http://20.111.54.16:8123')

# send request after the proxy in the client session
response = cn.get('https://httpbin.org/ip').json()['origin']
print(response)
```
`use build request for high performance`

```python3
import fiberhttp

cn = fiberhttp.client()

# build request with this format
request = fiberhttp.build('GET', 'httpbin.org', '/ip')

# send request after build it
response = cn.send('httpbin.org', request).json()
```

`create connection with host before send request to reduce response time`

```python3
import fiberhttp

cn = fiberhttp.client()

request = fiberhttp.build('GET', 'httpbin.org', '/ip')
cn.connect('httpbin.org')

response = cn.send('httpbin.org', request).text()
print(response)
```

`use build, create connection with proxies`
```python3
import fiberhttp

cn = fiberhttp.client_proxy('http://username:password@host:port')

# if the proxy has authentication, you must include the proxy_auth argument, which can be obtained from the client
request = fiberhttp.build_proxy('GET', 'httpbin.org', '/ip', proxy_auth=cn.proxy_auth)

# connect befor send not required; but its better for high peformance
cn.connect('httpbin.org')

response = cn.send('httpbin.org', request).text()
print(response)
```
