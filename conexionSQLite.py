import sqlite3

from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QTableWidgetItem


class ConexionSQLite:
    def __init__(self):
        self.conexion = sqlite3.connect('base_datos.db')
        self.cursor = self.conexion.cursor()

    def cargar_datos_en_tabla(self, tabla):
        query = "SELECT id, nombre, suscriptores, categoria, enlace FROM base_datos"
        resultado = self.cursor.execute(query).fetchall()
        tabla.setRowCount(0)
        for fila_num, fila_datos in enumerate(resultado):
            tabla.insertRow(fila_num)
            for col_num, dato in enumerate(fila_datos):
                tabla.setItem(fila_num, col_num, QTableWidgetItem(str(dato)))

        tabla.setColumnHidden(0, True) # esconde el id

    def insertar_canal(self, nombre, suscriptores, categoria, enlace):

        try:
            # Verificar si el nombre ya existe en la tabla
            query = "SELECT nombre FROM base_datos WHERE nombre = ?"
            resultado = self.cursor.execute(query, (nombre,))
            fila= resultado.fetchone()

            if fila is not None:
                # El nombre ya existe, salir
                return False

            else:
                self.cursor.execute("INSERT INTO base_datos (nombre, suscriptores, categoria, enlace) VALUES (?, ?, ?, ?)", (nombre, suscriptores, categoria, enlace))
                self.conexion.commit()
                return True

        except sqlite3.Error:
            return False

    def buscar_canal_tabla(self, tabla, nombre):
        query = "SELECT id, nombre, suscriptores, categoria, enlace FROM base_datos WHERE nombre = ?" # crea la consulta SQL para buscar los canales por nombre
        resultado = self.cursor.execute(query, (nombre,)) # ejecuta la consulta con el nombre recibido como parámetro
        tabla.setRowCount(0)
        for fila_num, fila_datos in enumerate(resultado):
            tabla.insertRow(fila_num)
            for col_num, dato in enumerate(fila_datos):
                tabla.setItem(fila_num, col_num, QTableWidgetItem(str(dato)))

        tabla.setColumnHidden(0, True) # esconde el id

    def borrar_canal_bd(self, nombre):

        query = "DELETE FROM base_datos WHERE nombre = ?" # crea una consulta SQL para eliminar el canal de la base de datos
        self.cursor.execute(query, (nombre,))
        self.conexion.commit() # guarda los cambios en la base de datos



    def buscar_canal_parametros(self, nombre):
        query = "SELECT nombre, suscriptores, categoria, enlace, id FROM base_datos WHERE nombre = ?"
        result = self.cursor.execute(query, (nombre,))
        row_data = result.fetchone() # Obtiene la primera fila del resultado

        if row_data is not None: # Si se encontró un resultado
            nombre = str(row_data[0])
            suscriptores = str(row_data[1])
            categoria = str(row_data[2])
            enlace = str(row_data[3])
            id = str(row_data[4])
            return nombre, suscriptores, categoria, enlace, id

        else:
            return "", "", "", "", "" # Si no se encontró un resultado, retorna ""

    def actualizar_canal_bd(self,id, nombre, suscriptores, categoria, enlace):
        query = "UPDATE base_datos SET nombre = ?, suscriptores = ?, categoria = ?, enlace = ? WHERE id = ?"
        self.cursor.execute(query, (nombre, suscriptores, categoria, enlace, id))
        self.conexion.commit()