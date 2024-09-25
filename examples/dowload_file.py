import fiberhttp

with open('downloaded_image.jpg', 'wb') as file:
    res = fiberhttp.get('https://httpbin.org/image')

    if res.status_code() == 200:
        
        file.write(res.content())
        print('The File has been saved !!')