from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import aiohttp

from requests.exceptions import MissingSchema

from timeit import default_timer
from tkinter import *
import asyncio
from rx import create, operators

from aiohttp import ClientSession
import requests

from bs4 import BeautifulSoup as bs

imagenes = []
nombreimagen = []
flaghaterminado = True;
maxnumberimg = 0




###

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


async def loop_imgs(url): # class Printer(rx.core.Observer):

    tasks = []
    img_fetch.start_time = dict()
    nombreimagen = []
    content = requests.get(url)
    soup = bs(content.text, 'html.parser')

    async with ClientSession() as session:

        for img in soup.find_all('img'):
            try:
                img_url = img['src']
                try:
                    img_response = requests.get(img_url)
                    try:

                         #   def on_next(self, v):
                         #       print(f'Recibido: {v}')


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

        def on_completed(self):
            print('Terminado')


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

'''
if __name__ == '__main__':
    #urls = 'https://medium.com/@ProxiesAPI.com/asynchronous-web-scraping-with-python-aiohttp-and-asyncio-83916022def7/'
    list = ['https://www.marca.com',
            'https://medium.com/@ProxiesAPI.com/asynchronous-web-scraping-with-python-aiohttp-and-asyncio-83916022def7/',
            'https://www.google.com/']
    #for urls in list:
    #    fetch_images(urls)

    fetch_images('https://www.marca.com')
'''

###
'''
async def descargarimages():
    print("Soy la coroutina")
    urls = [
        'https://www.marca.com/',

    ]
    global imgs
    global nombreimagen
    global maxnumberimg
    # imgs[0]= "dffsdfde"
    for url in urls:
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'html.parser')
        i = 0
        maxnumberimg = len(soup.find_all('img'))
        # print("Length"+ str((len(soup.find_all('img')))))
        # input("Pausa:")
        for img in soup.find_all('img'):
            img_url = img['src']
            try:
                nombreimagen.append(img_url.split("/")[-1])
                print(nombreimagen[i])
                i += 1
                print("He cogido imagens")
                imgs.append(requests.get(img_url))
                await asyncio.sleep(0)

            except:
                pass

    print("Image: " + str(len(imgs)))
    print("Finalizacion descarga")

    global flaghaterminado
    flaghaterminado = False
    print("Flag: " + str(flaghaterminado))
    # with open(f'downloaded_images/Imagendefinitiva.jpg', 'wb') as f:
    #    f.write(imgs[15].content)

'''





class App:
    def __init__(self):
        asyncio.run(self.Inicializacion())

    def Inicializacion(self):
        self.window = Tk()
        self.window.title("Paradigmas")
        self.window.geometry('350x300')

        self.lbl = Label(self.window, text="      URL a procesar           ", padx=10, pady=5)
        self.lbl.grid(column=0, row=0)

        self.txt = Entry(self.window, width=30)
        self.txt.grid(column=1, row=0)
        print(self.txt)
        #command=await asyncio.ensure_future(self.searchButton)
        self.btn = Button(self.window, text="Buscar", command=self.routine1, height=1, width=15)
        print("Esto sigue?")
        self.btn.grid(column=1, row=1)
        print("Antes de bucle")
        var = StringVar()
        self.lb = Listbox(self.window, listvariable=var, height=10, width=20)
        self.lb.grid(column=0, row=2)
        i = 0
        self.progress = 0
        #LLAMAR FUNCIONA ASINCRONA BUCLE

        self.progress_bar = ttk.Progressbar(orient="horizontal", length=150, mode="determinate")
        self.progress_bar["value"] = self.progress
        self.label = Label(text="Se encontraron x imágenes")
        self.progress_bar.grid(column=1, row=3)
        self.label.grid(column=1, row=4)
        self.window.mainloop()
        ########################3

    def routine1(self):
        print("TXT value:" + str(self.txt.get() ))
        fetch_images(([self.txt.get()]).pipe(
            operators.map(lambda s: s.upper()),
            operators.map(lambda s: f'En mayúscula: {s}')
        ).subscribe(lambda v: print(f'Recibido: {v}')))


if __name__ == '__main__':
    App()

