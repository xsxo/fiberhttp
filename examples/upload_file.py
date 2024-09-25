import fiberhttp

with open('downloaded_image.jpg', 'rb') as file:
    res = fiberhttp.post('https://httpbin.org/post', data={'file': file.read()})

    if res.status_code() == 200:
        print(res.text())
        print('The File has been uploaded !!')