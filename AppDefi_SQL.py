import datetime as dt
import sqlite3 as sql
import pandas as pd

"""Igual a la hora de crear la tabla control_pesos habria 
que cambiar el formato de fecha y ponerle TEXT, 
TIMESTAMP es un sello de fecha que va desde 1970, milisegundos desde
"""
def creacion_database():
    conexion = sql.connect("Tabla_Definicion.db")
    cursor = conexion.cursor()
    conexion.commit()
    conexion.close()

def creacion_tabla():
    conexion = sql.connect("Tabla_Definicion.db")
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE control_pesos(
                   Fecha TIMESTAMP,
                   Peso  DOUBLE,
                   Peso_Dia_anterior DOUBLE,
                   Peso_Promedio_Semana_Anterior DOUBLE,
                   Peso_VS_DiaAnterior DOUBLE,
                   Peso_VS_SemanaAnterior DOUBLE,
                   IMC DOUBLE,
                   Calorias_Entreno INT,
                   Cardio_TF BOOLEAN,
                   Calorias_Cardio INT,
                   Calorias_totales INT)
    """)
    conexion.commit()
    conexion.close()

def insertar_fila(fecha,peso, estatura, tiempo_entreno, cardio, tiempo_cardio,edad):
    conexion = sql.connect("Tabla_Definicion.db")
    cursor = conexion.cursor()
    MET_gym = 6
    MET_cardio = 4.5
    instruccion = f"""INSERT INTO control_pesos VALUES (
    '{fecha}', {peso},{peso-0.7},{round(0,2)},{round(peso-(peso+0.7),2)},{round(0,2)},{peso/(estatura/100)},
    {((round(MET_gym*3.5*peso)/200)*tiempo_entreno,2)},{cardio},{round(tiempo_cardio*((MET_cardio*3.5*peso)/200),2)},
    {((round((MET_gym*3.5*peso)/200)*tiempo_entreno)+(tiempo_cardio*((MET_cardio*3.5*peso)/200))+((10*peso)+(6.25*estatura)-(5*(edad)+5)),2)}
    )"""
    cursor.execute(instruccion)
    conexion.commit()
    conexion.close()

def insertar_variasfilas(añadir_varios_datos):
    conexion = sql.connect("Tabla_Definicion.db")
    cursor = conexion.cursor()
    cursor.executemany('INSERT INTO control_pesos VALUES (?,?,?,?,?,?,?,?,?,?,?)', añadir_varios_datos)
    conexion.commit()
    conexion.close()

def borrar_fila(condicion_fecha):
    conexion = sql.connect('Tabla_Definicion.db')
    cursor = conexion.cursor()
    instruccion = f'DELETE FROM control_pesos WHERE Fecha = "{condicion_fecha}"'
    cursor.execute(instruccion)
    conexion.commit()
    conexion.close()

def lectura_filas():
    conexion = sql.connect('Tabla_Definicion.db')
    cursor = conexion.cursor()
    instruccion = 'SELECT * FROM control_pesos ORDER BY Fecha DESC'
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return datos

def filtrado_tabla(): 
    conexion = sql.connect('Tabla_Definicion.db')
    cursor = conexion.cursor()
    tipo_filtrado = input('El tipo de filtrado que quieres realizar es filas o columnas o ambos? (escribe: "f" o "c"): ')
    if tipo_filtrado == 'c':
        columna1 = input('Introduce la primera columna: ')
        columna2 = input('Introduce la segunda columna: ')
        instruccion = f'SELECT {columna1}, {columna2} FROM control_pesos ORDER BY Fecha DESC'

    if tipo_filtrado == "f":
        eleccion = int(input('Escoge un tipo de filtrado:\n 1-Filtrado "="\n 2-Filtrado Between\n 3-Filtrado "> o <"\n    -->'))
        if eleccion == 1:
            formato_ejemplo = dt.datetime.now().strftime('%Y-%m-%d')
            fecha_formato = input(f'Cual es la fecha que quieres introducir (ejemplo:{formato_ejemplo}): ')
            instruccion = f'SELECT * FROM control_pesos WHERE Fecha = "{fecha_formato}"'
        if eleccion == 2:
            formato_ejemplo = dt.datetime.now().strftime('%Y-%m-%d')
            fecha_inicial = input(f'Inserta la fecha INICIAL (ejemplo: {formato_ejemplo}): ')
            fecha_final = input(f'Inserta la fecha Final (ejemplo: {formato_ejemplo}): ')
            instruccion = f'SELECT * FROM control_pesos WHERE Fecha BETWEEN "{fecha_inicial}" AND "{fecha_final}" ORDER BY Fecha DESC'
        if eleccion == 3:
            operacion = input('Filtrar por "mayor" o "menor": ').lower()
            if operacion == "mayor":
                formato_ejemplo = dt.datetime.now().strftime('%Y-%m-%d')
                fecha_formato = input(f'Cual es la fecha que quieres introducir (ejemplo: {formato_ejemplo}): ')
                instruccion = f'SELECT * FROM control_pesos WHERE Fecha > "{fecha_formato}" ORDER BY Fecha DESC'
            if operacion == "menor":
                formato_ejemplo = dt.datetime.now().strftime('%Y-%m-%d')
                fecha_formato = input(f'Cual es la fecha que quieres introducir (ejemplo: {formato_ejemplo}): ')
                instruccion = f'SELECT * FROM control_pesos WHERE Fecha < "{fecha_formato}" ORDER BY Fecha DESC'
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conexion.commit()
    conexion.close()
    print(datos)

def nombre_columnas():
    conexion = sql.connect('Tabla_Definicion.db')
    cursor = conexion.cursor()
    instruccion = 'SELECT name FROM pragma_table_info("control_pesos")'
    cursor.execute(instruccion)
    columnas = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return columnas

def lanza_querys(query):
    conexion = sql.connect('Tabla_Definicion.db')
    cursor = conexion.cursor()
    instruccion = query
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return datos

def auxilia_consultas(columna, fecha):
    conexion = sql.connect('Tabla_Definicion.db')
    cursor = conexion.cursor()
    instruccion = f'SELECT {columna} FROM control_pesos WHERE Fecha = "{fecha}"'
    cursor.execute(instruccion)
    peso = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return peso
    


   
"""if __name__ == '__main__':
    creacion_tabla()"""