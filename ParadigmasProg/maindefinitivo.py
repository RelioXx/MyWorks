from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import aiohttp

from requests.exceptions import MissingSchema
import rx
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
print("Before")
url = None
async def img_fetch(img_url, session):
    img_fetch.start_time[img_url] = default_timer()

    async with session.get(img_url) as response:
        r = await response.read()
        elapsed = default_timer() - img_fetch.start_time[img_url]

        #imagenes.append(img_url.split("/")[-1])
        imagenes.append(img_url)
        #imagenes.append(response)
        print("He cogido imagens")


async def loop_imgs(o,s):
    url = 'https://www.elmundo.es'
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
            o.on_next(img_url.split("/")[-1])
            if img_url[:1] == '/':
                print("Appending url " + url + " + " + img_url)
                img_url = url + img_url

            task = asyncio.ensure_future(img_fetch(img_url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)


def fetch_images(o,s):

    global imagenes
    urls= "https://www.elmundo.es"
    start_time = default_timer()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(loop_imgs(o,s))
    loop.run_until_complete(future)

    tot_elapsed = default_timer() - start_time
    print('Total time taken : ' + str(tot_elapsed))

    print("Image: " + str(len(imagenes)))
    print("Finalizacion descarga")
    print(imagenes)

class Printer(rx.core.Observer, object):
    def __init__(self, outer_instance):
        self.outer_instance = outer_instance
        self.outer_instance.somemethod()

    def on_next(self, v):
        print(f'Recibido: {v}')
        #print("Object: "+ str(self.varsf))

        self.lb.insert(v)
        self.lb.get(ACTIVE)


    def on_completed(self):
        print('Terminado')



class App:

    def __init__(self):
        print("App created")
        #(self.Inicializacion())

    varsf = 1
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


    def insertimage(self):
        print("EY QUE TAL GENTE")
      #  tkapp.lb.insert(v)
    # tkapp.lb.get(ACTIVE)


    def routine1(self):
        global url
        url = self.txt.get()
        print("TXT value:" + str(self.txt.get() ))
        rx.create(fetch_images).subscribe(Printer(self))


class Outer(object):

    def createInner(self):
        return Outer.Inner(self)

    class Inner(object):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.outer_instance.somemethod()

        def inner_method(self):
            self.outer_instance.anothermethod()

if __name__ == '__main__':
    global tkapp
    tkapp = App()
    tkapp.Inicializacion()
    print ("After")

