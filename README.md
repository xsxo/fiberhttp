# fiberhttp is high performance and simple HTTP library.

source code: [github](https://github.com/xsxo/fiberhttp/)<br/>
pypi project: [pypi](https://pypi.org/project/fiberhttp/)<br/>

install fiberhttp library on windows/linux/macos/other_os...<br/>
```bash
pip install fiberhttp
```
how to use:<br/>
```python3
# 1 import fiberhttp library
import fiberhttp

# 2 create client to save your connections session
cn = fiberhttp.client(timeout=10)
cn_without_timeout = cn()

# 3 send http request
response = cn.get('https://httpbin.org/ip')

# 4 take response with any format
print(response.json()['origin'])
print(response.text())
print(response.body())
print(response.headers().get('User-Agent'))

# 5 close connection after finish
cn.close_host('httpbin.org')

# 6 close all connections in the client
cn.close()
```

send http request directly, without keep connect session<br/>

```python3
import fiberhttp

# send http request without client
response = fiberhttp.get('https://httpbin.org')
print(response.text())
```

**soon fiberhttp will support proxies HTTP, HTTPS, SOCKS4, SOCKS5**<br/>
