from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
import sys
import random
import string
from conexionSQLite import *
from conexionSQLiteUsuarios import ConexionSQLiteUsuarios


class Ventana(QMainWindow):
    def __init__(self,nombre_base_datos):
        super().__init__()
        loadUi('interfaz1.ui', self)  # carga la interfaz de usuario desde el archivo .ui
        self.nombre_base_datos = nombre_base_datos
        self.conexion = ConexionSQLite(self.nombre_base_datos)
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

        self.bt_menu.clicked.connect(self.mover_menu)

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
        self.id_act = ''

        self.bt_buscar_consultar.clicked.connect(self.consultar)

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


    def mover_menu(self):
        width = self.frame_control.width()
        normal = 0
        if width == 0:
            extender = 200
        else:
            extender = normal
        self.animacion = QPropertyAnimation(self.frame_control, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)

        self.animacion.start()
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
        categoria = self.line_categoria_reg.text().upper() # line edit de la categoria a registrar
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
            self.conexion.buscar_canal_tabla(self.tabla_borrar, nombre.upper())
        else:
            self.label_borrar_estado.setText("No se ha ingresado un parámetro de búsqueda")

    def borrar_canal(self):
        fila_seleccionada = self.tabla_borrar.currentRow() # obtiene la fila seleccionada en la tabla
        nombre = self.tabla_borrar.item(fila_seleccionada, 1).text() # obtiene el nombre del canal en la columna 0 de la fila seleccionada

        self.conexion.borrar_canal_bd(nombre) # llama el metodo para borrar el canal de la base de datos
        self.tabla_borrar.removeRow(fila_seleccionada) # elimina la fila de la tabla
        self.bt_borrar.setEnabled(False) # deshabilita el botón de borrar después de eliminar el canal

    def seleccionar_fila(self, row, column):
        self.bt_borrar.setEnabled(True) # habilita el botón de borrar cuando se selecciona una fila de la tabla


    def buscar_actualizar(self):
        nombre_a_buscar = self.line_buscar_act.text()
        nombre, suscriptores, categoria, enlace, id = self.conexion.buscar_canal_parametros(nombre_a_buscar)
        if (nombre != ""):
            self.line_nombre_act.setText(nombre)
            self.line_suscriptores_act.setText(suscriptores)
            self.line_categoria_act.setText(categoria)
            self.line_enlace_act.setText(enlace)
            self.id_act = id
            self.label_act_estado.setText("Canal encontrado")
        else:
            self.label_act_estado.setText("Canal no encontrado")
            self.line_nombre_act.clear()
            self.line_suscriptores_act.clear()
            self.line_categoria_act.clear()
            self.line_enlace_act.clear()

    def actualizar(self):
        self.label_act_estado.setText("")
        nombre = self.line_nombre_act.text()
        suscriptores = self.line_suscriptores_act.text()
        categoria = self.line_categoria_act.text().upper()
        enlace = self.line_enlace_act.text()
        if (nombre != "" and suscriptores != "" and categoria != "" and enlace != ""):
            self.conexion.actualizar_canal_bd(self.id_act, nombre, suscriptores, categoria, enlace)
            self.label_act_estado.setText("Canal actualizado")
        else:
            self.label_act_estado.setText("No se pudo actualizar el canal")

    def consultar(self):
        nombre_a_buscar = self.line_buscar_consultar.text()
        nombre, suscriptores, categoria, enlace, id = self.conexion.buscar_canal_parametros(nombre_a_buscar)
        if(nombre != "" and suscriptores != "" and categoria != "" and enlace != ""):
            self.label_nombre_cons.setText(nombre)
            self.label_suscriptores_cons.setText(suscriptores)
            self.label_categoria_cons.setText(categoria)
            self.label_enlace_cons.setText(enlace)
            self.label_consultar_estado.setText("Canal encontrado")
        else:
            self.label_consultar_estado.setText("No se encontró el canal")
            self.label_nombre_cons.clear()
            self.label_suscriptores_cons.clear()
            self.label_categoria_cons.clear()
            self.label_enlace_cons.clear()

class IniciarSesion(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('iniciosesion.ui',self) # carga la interfaz de inicio de sesion desde el archivo .ui
        self.conexion = ConexionSQLiteUsuarios()
        self.ventana = None
        self.bt_ingresar_usuario.clicked.connect(self.abrir_menu)
        self.bt_ir_a_pagina_registrar_usuario.clicked.connect(self.ir_a_pagina_registrar_usuario)
        self.bt_registrar_usuario.clicked.connect(self.registrar_usuario)
        self.bt_ir_a_pagina_iniciar_sesion.clicked.connect(self.ir_a_pagina_iniciar_sesion)
        # quita el borde de la ventana
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        self.center()
        # conecta la señal clicked del botón bt_cerrar al método close de la ventana
        self.bt_cerrar.clicked.connect(self.close)

        # conecta la señal clicked del botón bt_ventana al método cambiar_estado_ventana
        self.bt_ventana.clicked.connect(self.cambiar_estado_ventana)

        # conecta la señal clicked del botón bt_min al método minimizar_ventana
        self.bt_min.clicked.connect(self.minimizar_ventana)

    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())
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
    def abrir_menu(self):
        usuario = self.line_nombre_usuario.text()
        clave = self.line_clave_usuario.text()
        if(usuario!= "" and clave != ""):
            inicioExitoso= self.conexion.el_usuario_y_clave_correctos(usuario,clave)

            if inicioExitoso==True:
                if self.ventana is None:
                    nombre_base_datos = self.conexion.base_de_datos_usuario(usuario)
                    self.ventana = Ventana(nombre_base_datos)


                    self.ventana.show()

                    iniciarSesion.hide()

                else:
                    self.ventana = None  # Discard reference, close window.
            else:
                self.label_estado_iniciarsesion.setText("Usuario o contraseña incorrectos")
        else:
            self.label_estado_iniciarsesion.setText("No se han completado todos los campos")

    def ir_a_pagina_registrar_usuario(self):
        # Obtiene el índice de la página a mostrar
        indice_pagina_registrar_usuario = self.stackedWidget.indexOf(self.page_registrarse)

        # Muestra la página
        self.stackedWidget.setCurrentIndex(indice_pagina_registrar_usuario)

    def ir_a_pagina_iniciar_sesion(self):
        # Obtiene el índice de la página a mostrar
        indice_pagina_iniciar_sesion = self.stackedWidget.indexOf(self.page_iniciarsesion)

        # Muestra la página
        self.stackedWidget.setCurrentIndex(indice_pagina_iniciar_sesion)

    def registrar_usuario(self):
        usuario = self.line_nom_usuario_registrar.text()
        clave = self.line_clave_usuario_registrar.text()
        nom_base_datos = usuario + str(random.randint(10000, 99999)) # el nombre de la nueva base de datos es el usuario con un entero aleatorio
        if (usuario != "" and clave != ""):
            if(self.conexion.base_de_datos_usuario(usuario)==""): # si no retorna un nombre, no existe ese usuario, se puede usar
                self.conexion.insertar_nuevo_usuario(usuario, clave, nom_base_datos)

                # Conexión a la base de datos
                conexion = sqlite3.connect(nom_base_datos + '.db')

                # Cursor para ejecutar sentencias SQL
                cursor = conexion.cursor()

                # Creación de la tabla con los parámetros especificados y celdas vacías por defecto
                cursor.execute('''CREATE TABLE base_datos
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NOMBRE TEXT DEFAULT '',
                 SUSCRIPTORES INTEGER DEFAULT 0,
                 CATEGORIA TEXT DEFAULT '',
                 ENLACE TEXT DEFAULT '')''')

                # Guardar los cambios y cerrar la conexión a la base de datos
                conexion.commit()
                conexion.close()

                self.label_estado_registrar.setText("Registro exitoso")
            else:
                self.label_estado_registrar.setText("El usuario ya existe, intente con otro nombre")
        else:
            self.label_estado_registrar.setText("No se han completado todos los campos")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    iniciarSesion = IniciarSesion()
    iniciarSesion.show()

    sys.exit(app.exec())
