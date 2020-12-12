from tkinter import *
from tkinter.ttk import Combobox


class App:
    def __init__(self):
        self.__contador = 0
        self.window = Tk()
        self.window.title = 'Aplicación Gráfica!'
        # window.maxsize(width=300, height=200)
        # window.minsize(width=100, height=120)
        # window.geometry('800x400')

        Label(text='Hola!', font=('Arial Bold', 36)).grid(column=0, row=0)
        self.text = Label(text='Esto sale más pequeño', font=('Arial', 24))
        self.text.grid(column=1, row=0)

        Button(text='Pulsa', width=35, command=self.buttonCount, pady=15).grid(column=0, row=1, columnspan=2)

        self.entry = Entry()
        self.entry.grid(column=0, row=2)
        Button(text='Pulsa', command=self.buttonEntry, pady=20).grid(column=1, row=2)

        self.combo = Combobox(values=['Cero', 'Uno', 'Dos', 'Tres', 'Cuatro'], state='readonly')
        self.combo.grid(column=0, row=3)
        self.combo.current(0)
        Button(text='Pulsa', command=self.buttonCombo).grid(column=1, row=3)

        self.window.mainloop()

    def buttonCount(self):
        self.__contador += 1
        self.text.configure(text=f'Has pulsado {self.__contador} veces')

    def buttonEntry(self):
        self.text.configure(text=f'El entry contiene: {self.entry.get()}')


    def buttonCombo(self):
        self.text.configure(text=f'El índice seleccionado es {self.combo.current()}, y su texto es: {self.combo.get()}')

if __name__ == '__main__':
    App()
