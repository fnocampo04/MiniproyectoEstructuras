import sqlite3
from PyQt6.QtWidgets import QTableWidgetItem


class ConexionSQLite:
    def __init__(self):
        self.conexion = sqlite3.connect('base_datos.db')
        self.cursor = self.conexion.cursor()

    def cargar_datos_en_tabla(self, tabla):
        query = "SELECT nombre, suscriptores, categoria, enlace FROM base_datos"
        resultado = self.cursor.execute(query).fetchall()
        tabla.setRowCount(0)
        for fila_num, fila_datos in enumerate(resultado):
            tabla.insertRow(fila_num)
            for col_num, dato in enumerate(fila_datos):
                tabla.setItem(fila_num, col_num, QTableWidgetItem(str(dato)))

    def insertar_canal(self, nombre, suscriptores, categoria, enlace):

        try:
            self.cursor.execute("INSERT INTO base_datos (nombre, suscriptores, categoria, enlace) VALUES (?, ?, ?, ?)", (nombre, suscriptores, categoria, enlace))
            self.conexion.commit()
            return True
        except sqlite3.Error:
            self.label_registro_estado.setText("Error al insertar datos con SQLite")
            return False

