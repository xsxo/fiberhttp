## About Benchmark
Benchmarks were conducted to compare the performance of fiberhttp with the most widely used libraries to demonstrate its efficiency.
The benchmarks were conducted on a local server to ensure a consistent network speed across all libraries.

All the files used for the comparison are available in the repository at the current path, you can run your own benchmark and display the results.

## Benchmark Scenario

100 threads and 100 connections are created to send 1,000,000 HTTP requests in record time. You'll notice that low-level libraries perform the fastest in the benchmarks.

|**Library**|**Results (Lower is Better)**|
|-----------|-------------------|
|FiberHTTP|1,000,000 HTTP Requests in 18 SEC'S|
|http.client|1,000,000 HTTP Requests in 92 SEC'S|
|AIOHTTP|1,000,000 HTTP Requests in 162 SEC'S|
|urllib3|1,000,000 HTTP Requests in 221 SEC'S|
|HTTPX|1,000,000 HTTP Requests in 332 SEC'S|
|HTTPX-ASYNC|1,000,000 HTTP Requests in 427 SEC'S|
|requests|1,000,000 HTTP Requests in 472 SEC'S|


```bash
fiberhttp Sent 1000000 HTTP Requests in 18 Second With 100 Threads
http.client Sent 1000000 HTTP Requests in 92 Second With 100 Threads
urllib3 Sent 1000000 HTTP Requests in 221 Second With 100 Threads
requests Sent 1000000 HTTP Requests in 472 Second With 100 Threads
httpx Sent 1000000 HTTP Requests in 332 Second With 100 Threads
httpx-async Sent 1000000 HTTP Requests in 427 Seconds With 100 Threads
aiohttp Sent 1000000 HTTP Requests in 162 Seconds With 100 Threads
```