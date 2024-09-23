## About Benchmark
Benchmarks were conducted to compare the performance of fiberhttp with the most widely used libraries to demonstrate its efficiency.

All the files used for the comparison are available in the repository at the current path, you can run your own benchmark and display the results.

## Benchmark Scenario
Ten threads are created for each library, running for 10 seconds. The library that sends the most requests within these 10 seconds is considered the highest performing.

|**library**|**result**|
|------------|--------------|
|fiberhttp|226 request in 10 sec and 10 threads|
|requests|200 request in 10 sec and 10 threads|
|httpx|165 request in 10 sec and 10 threads|
|http.client|154 request in 10 sec and 10 threads|

The difference might be somewhat subtle, but when sending a large number of requests, you'll see significant differences.
