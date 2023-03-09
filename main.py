from PyQt6.QtWidgets import QMainWindow, QApplication,QSizeGrip, QPushButton
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QPoint
import sys

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('interfaz1.ui', self)  # carga la interfaz de usuario desde el archivo .ui

        # quita el borde de la ventana
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)



        # conecta la señal clicked del botón bt_cerrar al método close de la ventana
        self.bt_cerrar.clicked.connect(self.close)

        # conecta la señal clicked del botón bt_ventana al método cambiar_estado_ventana
        self.bt_ventana.clicked.connect(self.cambiar_estado_ventana)

        # conecta la señal clicked del botón bt_min al método minimizar_ventana
        self.bt_min.clicked.connect(self.minimizar_ventana)

        # maximiza la ventana al iniciar la aplicación
        self.showMaximized()

        # conecta la señal clicked del botón pushButton al método ir_a_pagina_datos
        self.pushButton.clicked.connect(self.ir_a_pagina_datos)

        # conecta la señal clicked del botón pushButton_2 al método ir_a_pagina_registrar
        self.pushButton_2.clicked.connect(self.ir_a_pagina_registrar)

        # conecta la señal clicked del botón pushButton_3 al método ir_a_pagina_borrar
        self.pushButton_3.clicked.connect(self.ir_a_pagina_borrar)

        # conecta la señal clicked del botón pushButton_4 al método ir_a_pagina_actualizar
        self.pushButton_4.clicked.connect(self.ir_a_pagina_actualizar)

        # conecta la señal clicked del botón pushButton_5 al método ir_a_pagina_consultar
        self.pushButton_5.clicked.connect(self.ir_a_pagina_consultar)



    def cambiar_estado_ventana(self):
        if self.isMaximized():
            # si la ventana está maximizada, la restaura
            self.showNormal()
        else:
            # si la ventana no está maximizada, la maximiza
            self.showMaximized()

    def minimizar_ventana(self): # minimizar la ventana
        self.showMinimized()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()


    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
        self.dragPos = event.globalPosition().toPoint()
        event.accept()



    def ir_a_pagina_registrar(self):
        # Obtiene el índice de la página a mostrar
        indice_pagina_registrar = self.stackedWidget.indexOf(self.page_registrar)

        # Muestra la página
        self.stackedWidget.setCurrentIndex(indice_pagina_registrar)

    def ir_a_pagina_datos(self):
        # Obtiene el índice de la página a mostrar
        indice_pagina_datos = self.stackedWidget.indexOf(self.page_datos)

        # Muestra la página
        self.stackedWidget.setCurrentIndex(indice_pagina_datos)

    def ir_a_pagina_borrar(self):
        # Obtiene el índice de la página a mostrar
        indice_pagina_borrar = self.stackedWidget.indexOf(self.page_borrar)

        # Muestra la página
        self.stackedWidget.setCurrentIndex(indice_pagina_borrar)

    def ir_a_pagina_actualizar(self):
        # Obtiene el índice de la página a mostrar
        indice_pagina_actualizar = self.stackedWidget.indexOf(self.page_actualizar)

        # Muestra la página
        self.stackedWidget.setCurrentIndex(indice_pagina_actualizar)

    def ir_a_pagina_consultar(self):
        # Obtiene el índice de la página a mostrar
        indice_pagina_consultar = self.stackedWidget.indexOf(self.page_consultar)

        # Muestra la página
        self.stackedWidget.setCurrentIndex(indice_pagina_consultar)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
