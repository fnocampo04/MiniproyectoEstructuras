
import sqlite3

class Comunicacion():
    def __init__(self):
        self.conexion = sqlite3.connect('base_datos.db')

    def inserta_canal(self, nombre, suscriptores, categoria):
        cursor = self.conexion.cursor()
