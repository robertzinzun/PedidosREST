from PyQt5.QtWidgets  import QApplication, QMainWindow, QPushButton
import sys



class Ventana (QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mi primer GUI')
        # agreganto otros widgets (controle)
        #crearo el widget
        boton= QPushButton ('Aceptar')
        #agregar (programar) el evento, todos los eventos terminan en 'ed'
        boton.clicked.connect(self.eventoBoton)

        #agregar el objeto a la ventana
        self.setCentralWidget(boton)
    def eventoBoton(self):
        print ('mnejando el evento')
if __name__=='__main__':
    app=QApplication(sys.argv)
    objVentana=Ventana()
    objVentana.show();
    app.exec()