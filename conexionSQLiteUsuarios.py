import sqlite3


class ConexionSQLiteUsuarios:
    def __init__(self):
        self.conexion = sqlite3.connect('usuarios.db')
        self.cursor = self.conexion.cursor()

    def el_usuario_y_clave_correctos(self, usuario, clave):
        query = "SELECT usuario,clave FROM usuarios WHERE usuario = ?"
        result = self.cursor.execute(query, (usuario,))
        row_data = result.fetchone() # Obtiene la primera fila del resultado

        if row_data is not None: # Si se encontró un resultado
            usuarioReal = str(row_data[0])
            claveReal = str(row_data[1])
            if(usuarioReal == usuario and claveReal == clave):
                return True

        else:
            return False

    def base_de_datos_usuario(self,usuario):
        query = "SELECT base_datos FROM usuarios WHERE usuario = ?"
        result = self.cursor.execute(query, (usuario,))
        row_data = result.fetchone() # Obtiene la primera fila del resultado

        if row_data is not None: # Si se encontró un resultado
            base_datos = str(row_data[0])
            return base_datos

        else:
            return ""

    def insertar_nuevo_usuario(self, usuario, clave, base_datos):
        self.cursor.execute("INSERT INTO usuarios (usuario, clave, base_datos) VALUES (?, ?, ?)", (usuario, clave, base_datos))
        self.conexion.commit()