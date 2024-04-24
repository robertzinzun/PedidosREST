from tkinter import *
from tkinter import ttk

class Aplicacion():
    def __init__(self):
        vSolicitudes = Tk()
        vSolicitudes.geometry('300x200')
        vSolicitudes.configure(bg='beige')
        ttk.Button(vSolicitudes, text='Salir', command=quit).pack(side=BOTTOM)
        vSolicitudes.title("GUI de Ejemplo")
        vSolicitudes.mainloop()

def main():
    ap=Aplicacion()
    return 0

if __name__=="__main__":
    main()