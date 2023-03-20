from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QMainWindow, QApplication, QSizeGrip, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QPoint
import sys

from conexionSQLite import *


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('interfaz1.ui', self)  # carga la interfaz de usuario desde el archivo .ui

        self.conexion = ConexionSQLite()
        self.conexion.cargar_datos_en_tabla(self.tabla_datos)
        self.conexion.cargar_datos_en_tabla(self.tabla_borrar)

        # ajusta las tablas al tamaño de la ventana
        self.tabla_datos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_borrar.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # deshabilita la edición de las tablas


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

        # conecta el evento clicked del botón bt_registrar a la función registrar_canal
        self.bt_registrar.clicked.connect(self.registrar_canal)

        # conecta la señal clicked del botón bt_refrescar al método refrescar_tabla
        self.bt_refrescar.clicked.connect(self.refrescar_tabla)

        self.bt_buscar_borrar.clicked.connect(self.buscar_borrar)

        self.bt_borrar.clicked.connect(self.borrar_canal)
        self.bt_borrar.setEnabled(False) # deshabilita el botón de borrar hasta que se seleccione una fila
        self.tabla_borrar.cellClicked.connect(self.seleccionar_fila) # conecta la señal de clic en una celda a la función seleccionar_fila

        self.bt_buscar_actualizar.clicked.connect(self.buscar_actualizar)

        self.bt_actualizar.clicked.connect(self.actualizar)

        self.nombre_actual = ''

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
        self.conexion.cargar_datos_en_tabla(self.tabla_borrar)

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

    def refrescar_tabla(self):
        self.conexion.cargar_datos_en_tabla(self.tabla_datos)
    def registrar_canal(self):
        nombre = self.line_nombre_reg.text() # line edit del nombre a registrar
        suscriptores = self.line_suscriptores_reg.text() # line edit de los suscriptores a registrar
        categoria = self.line_categoria_reg.text() # line edit de la categoria a registrar
        enlace = self.line_enlace_reg.text() # line edit del enlace a registrar

        if (nombre != '' and suscriptores != '' and categoria != '' and enlace != ''): # verifica que los campos no estan vacios
            reg_exitoso = self.conexion.insertar_canal(nombre, suscriptores, categoria, enlace) # el metodo inserta el canal en la base de datos
            if(reg_exitoso == True):
                self.label_registro_estado.setText("Canal registrado correctamente")
                self.line_nombre_reg.clear()
                self.line_suscriptores_reg.clear()
                self.line_categoria_reg.clear()
                self.line_enlace_reg.clear()
            elif(reg_exitoso == False):
                self.label_registro_estado.setText("Error en la base de datos. El nombre puede estar en uso, intente nuevamente")

        else:
            self.label_registro_estado.setText("No se han completado todos los campos")

    def buscar_borrar(self): # metodo para la pagina borrar para filtrar un canal

        nombre = self.line_buscar_borrar.text()
        if(nombre != ''): # verifica que si haya escrito algo
            self.conexion.buscar_canal_tabla(self.tabla_borrar, nombre)
        else:
            self.label_borrar_estado.setText("No se ha ingresado un parámetro de búsqueda")

    def borrar_canal(self):
        fila_seleccionada = self.tabla_borrar.currentRow() # obtiene la fila seleccionada en la tabla
        nombre = self.tabla_borrar.item(fila_seleccionada, 1).text() # obtiene el nombre del canal en la columna 0 de la fila seleccionada
        #id = self.tabla_borrar.item(fila_seleccionada, 0).text()  # Obtener el valor de la columna ID para la fila seleccionada
        self.conexion.borrar_canal_bd(nombre) # llama el metodo para borrar el canal de la base de datos
        self.tabla_borrar.removeRow(fila_seleccionada) # elimina la fila de la tabla
        self.bt_borrar.setEnabled(False) # deshabilita el botón de borrar después de eliminar el canal

    def seleccionar_fila(self, row, column):
        self.bt_borrar.setEnabled(True) # habilita el botón de borrar cuando se selecciona una fila de la tabla


    def buscar_actualizar(self):
        nombre_a_buscar = self.line_buscar_act.text()
        nombre, suscriptores, categoria, enlace = self.conexion.buscar_canal_parametros(nombre_a_buscar)
        if (nombre != ""):
            self.line_nombre_act.setText(nombre)
            self.line_suscriptores_act.setText(suscriptores)
            self.line_categoria_act.setText(categoria)
            self.line_enlace_act.setText(enlace)
            self.nombre_actual = nombre_a_buscar
        else:
            self.label_act_estado.setText("Canal no encontrado")
            self.line_nombre_act.clear()
            self.line_suscriptores_act.clear()
            self.line_categoria_act.clear()
            self.line_enlace_act.clear()

    def actualizar(self):

        nombre = self.line_nombre_act.text()
        suscriptores = self.line_suscriptores_act.text()
        categoria = self.line_categoria_act.text()
        enlace = self.line_enlace_act.text()
        if (nombre != "" and self.nombre_actual != ""):
            self.conexion.borrar_canal_bd(self.nombre_actual)
            self.conexion.insertar_canal(nombre,suscriptores, categoria, enlace)
            self.nombre_actual = ''




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
