# FiberHTTP [![Supported Versions](https://img.shields.io/pypi/pyversions/fiberhttp.svg)](https://pypi.org/project/fiberhttp)

`FiberHTTP` High Performance HTTP Requests Library<br/>

![GIF](media/1725894429188248.gif)

The [benchmarks](https://github.com/xsxo/fiberhttp/tree/main/benchmarks) folder contains comparisons between `FiberHTTP` and other well-known libraries such as `requests`, `httpx`, `http.client`, and others. You will notice that `FiberHTTP` outperforms them every time<br/>


## Fiberhttp might not for you

Fiberhttp is designed to provide high performance but lacks many features like:

**missing Features**:
- No Support streaming requests
- No Support redirects requests
- No Support compressed requests
- No Support chunked requests

All these features are not supported by the library for the purpose of improving performance.<br/>
If these features are important to you, and you value compatibility and functionality over performance, then the requests library might be a better choice for you.


## Features:
- Keep-alive (socket connection)
- Upload & Download Multi Files
- Prepare bytes request before send
- Create Connection with server before send the request
- High-performance SSL/TLS handshake, verify
- Reading responses in various formats such as JSON, headers, Cookies

## Benchmarks
Benchmarks Codes: [benchmarks](https://github.com/xsxo/fiberhttp/tree/main/benchmarks)

|**Library**|**Results (Lower is Better)**|
|-----------|-------------------|
|FiberHTTP|1,000,000 HTTP Requests in 18 SEC'S|
|http.client|1,000,000 HTTP Requests in 92 SEC'S|
|AIOHTTP|1,000,000 HTTP Requests in 162 SEC'S|
|urllib3|1,000,000 HTTP Requests in 221 SEC'S|
|HTTPX|1,000,000 HTTP Requests in 332 SEC'S|
|HTTPX-ASYNC|1,000,000 HTTP Requests in 427 SEC'S|
|requests|1,000,000 HTTP Requests in 472 SEC'S|

## How to use
install Fiberhttp (supported all os systems)
```bash
pip install fiberhttp
```

`with client session`
```python3
import fiberhttp

# create client session with timeout
# ! timeout arg not requierd
cn = fiberhttp.Client(timeout=10)

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
cn = fiberhttp.Client_Proxy('http://20.111.54.16:8123')

# send request after the proxy in the client session
response = cn.get('https://httpbin.org/ip').json()['origin']
print(response)
```


`use prepare request to get high performance`

```python3
import fiberhttp

cn = fiberhttp.Client()

# prepare request with this format
request = fiberhttp.Request('GET', 'https://httpbin.org/ip')

# send request after prepare it
response = cn.send(request).json()
```


`create connection with host before send request to reduce response time`

```python3
import fiberhttp

cn = fiberhttp.Client()

request = fiberhttp.Request('GET', 'https://httpbin.org/ip')

# create connection with host
cn.connect('httpbin.org')

response = cn.send(request).text()
print(response)
```
