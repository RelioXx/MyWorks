import asyncio
from timeit import default_timer
from aiohttp import ClientSession
import requests

from bs4 import BeautifulSoup as bs

imagenes = []
"""
async def fetch(url, session):
    fetch.start_time[url] = default_timer()
    async with session.get(url) as response:
        r = await response.read()
        elapsed = default_timer() - fetch.start_time[url]
        print(url + ' took ' + str(elapsed))
        return r
async def fetch_all(urls):
    tasks = []
    fetch.start_time = dict()
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)
"""

async def img_fetch(img_url, session):
    img_fetch.start_time[img_url] = default_timer()

    async with session.get(img_url) as response:
        r = await response.read()
        elapsed = default_timer() - img_fetch.start_time[img_url]

        #imagenes.append(img_url.split("/")[-1])
        imagenes.append(img_url)
        #imagenes.append(response)
        print("He cogido imagens")


async def loop_imgs(url):

    tasks = []
    img_fetch.start_time = dict()

    content = requests.get(url)
    soup = bs(content.text, 'html.parser')

    async with ClientSession() as session:

        for img in soup.find_all('img'):
            try:
                img_url = img['src']
                try:
                    img_response = requests.get(img_url)
                    try:
                        with open(f'downloaded_images/{img_url.split("/")[-1]}', 'wb') as f:
                            f.write(img_response.content)
                    except OSError:
                        pass
                    except IOError:
                        pass
                except:
                    pass
            except:
                print("! - NAY")
                continue

            print("YAY")
            if img_url[:1] == '/':
                print("Appending url " + url + " + " + img_url)
                img_url = url + img_url

            task = asyncio.ensure_future(img_fetch(img_url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)


def fetch_images(urls):

    global imagenes

    start_time = default_timer()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(loop_imgs(urls))
    loop.run_until_complete(future)

    tot_elapsed = default_timer() - start_time
    print('Total time taken : ' + str(tot_elapsed))

    print("Image: " + str(len(imagenes)))
    print("Finalizacion descarga")
    print(imagenes)


if __name__ == '__main__':
    #urls = 'https://medium.com/@ProxiesAPI.com/asynchronous-web-scraping-with-python-aiohttp-and-asyncio-83916022def7/'

    #for urls in list:
    #    fetch_images(urls)

    fetch_images('https://www.elmundo.es')

