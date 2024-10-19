from tkinter import ttk
from tkinter import *
from tkinter import Text



import os


import sqlite3 as sql
import AppDefi_SQL as app
from AppDefi_SQL import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Incluir dos pack mas donde se vean las respuestas de la consola y otra donde esten los graficos.
#TODO
#Boton de actualizar actualmente sin uso, tengo que implementarlo
#Generar una lista con user: y chatbot:
#Añadir el grafico para diferentes medidas, peso, evolucion de las calorias y demas

#Futuros desarrollos
#Incluir fotografia y comentario con IA sobre la evolucion del fisico, se necesitaran labelframe mas, necesitariamos dataset con los label
#Incluir un chatbot de un modelo desde 0 donde el usuario pueda preguntar cosas sobre el gym puede ser modelo fine tuned con info gym


TABLA = 'Tabla_Definicion.db'

class Pesos:

    def __init__(self,root):

        self.wind = root
        self.wind.title('App Definicion 2024')
        self.wind.geometry("1750x1150")

        frame1 = LabelFrame(self.wind, text='Datos Pesos por fecha', font=("Helvetica", 14)) 

        frame2 = LabelFrame(self.wind, text='Filtrado para los pesos', font=("Helvetica", 14))

        frame3 = LabelFrame(self.wind, text='Graficado', font=("Helvetica", 14))
        self.frame3 = frame3

        frame4 = LabelFrame(self.wind, text='Preguntas Chatbot', font=("Helvetica", 14))


        #Voy a tener que cambiar la estructura y no hacerlo con pack sino con grid() o place() que es mucho mas versatil
        #frame1.pack(fill='both', expand='no',padx=30,pady=20, side=TOP)
        #frame2.pack(fill='x', expand='no', side=LEFT)
        #frame3.pack(fill='both', expand='yes',padx=20,pady=10,side=BOTTOM)
        frame1.place(x=100,y=10, width=1600)
        frame2.place(x=100, y=280, width=750)
        frame3.place(x=900, y=280, width=800, height=793)
        frame4.place(x=100, y=600, width=750)

        self.trv = ttk.Treeview(frame1, columns= (1,2,3,4,5,6,7,8,9,10,11), show='headings', height=10)
        self.trv.grid()

        #Importante, hay que intentar que al tirar una query solo muestre las columnas de la query
        columnas = app.nombre_columnas()
        for numero, encabezado in enumerate(columnas):
            self.trv.heading(numero+1,text=list(encabezado))
            if len(encabezado[0]) > 18:
                anchura = 200
            else:
                anchura = 110
            self.trv.column(numero+1, width=anchura)
        self.consulta()

        self.text = Text(frame4, background="white", width=140, height=25)
        self.text.config(state="disable")
        self.text.grid()


        lbl1 = Label(frame2, text='Fecha del peso', width= 20)
        lbl1.grid(row=0, padx=8, pady=5)
        self.ent1 = Entry(frame2)
        self.ent1.grid(row=0, column=1, padx=8, pady=5)

        lbl2 = Label(frame2, width= 20)
        lbl2.grid(row=1, padx=8, pady=5)

        lbl3 = Label(frame2, text='Peso', width= 20)
        lbl3.grid(row=1, padx=8, pady=5)
        self.ent2 = Entry(frame2)
        self.ent2.grid(row=1, column=1, padx=8, pady=5)

        lbl4 = Label(frame2, width= 20)
        lbl4.grid(row=2, padx=8, pady=5)

        lbl5 = Label(frame2, text='Tiempo entreno', width= 20)
        lbl5.grid(row=2, padx=8, pady=5)
        self.ent3 = Entry(frame2)
        self.ent3.grid(row=2, column=1, padx=8, pady=5)

        lbl6 = Label(frame2, width= 20)
        lbl6.grid(row=3, padx=8, pady=5)

        lbl7 = Label(frame2, text='Cardio 0/1', width= 20)
        lbl7.grid(row=3, padx=8, pady=5)
        self.ent4 = Entry(frame2)
        self.ent4.grid(row=3, column=1, padx=8, pady=5)

        lbl8 = Label(frame2, width= 20)
        lbl8.grid(row=4, padx=8, pady=5)

        lbl9 = Label(frame2, text='Tiempo Cardio', width= 20)
        lbl9.grid(row=4, padx=8, pady=5)
        self.ent5 = Entry(frame2)
        self.ent5.grid(row=4, column=1, padx=8, pady=5)

        lbl10 = Label(frame2, width= 20)
        lbl10.grid(row=5, padx=8, pady=5)

        lbl11 = Label(frame2, text='Edad', width= 20)
        lbl11.grid(row=5, padx=8, pady=5)
        self.ent6 = Entry(frame2)
        self.ent6.grid(row=5, column=1, padx=8, pady=5)

        lbl12 = Label(frame2, width= 20)
        lbl12.grid(row=6, padx=8, pady=5)

        btt1 = Button(frame2, text='Agregar',command=self.agregar, width=12, height=2)
        btt1.grid(row=0, column=4)

        btt2 = Button(frame2, text='Filtrar', command=self.filtrar, width=12, height=2)
        btt2.grid(row=0, column=5)

        btt3 = Button(frame2, text='Actualizar', width=12, height=2)
        btt3.grid(row=1, column=4)

        btt4 = Button(frame2, text='Eliminar',command=self.eliminar, width=12, height=2)
        btt4.grid(row=1, column=5)

        btt5 = Button(master=frame3,text="cerrar",bg="red",command=self.cerrar, width=10, height=3, font=15)
        btt5.pack(side="bottom")

        btt6 = Button(master=frame3,text="Actualizar",command=self.actualizar_grafico, width=12, height=2)
        btt6.pack(side="top")


        self.ent7 = Entry(frame4)
        self.ent7.place(x=10, y=415, width=420)
        btt7 = Button(master=frame4,text="Insertar texto", command=self.insert_text, width=15, height=2)
        btt7.grid()

        self.graficar()
    

    def graficar(self):
            
        datos = lectura_filas()
        num_regis = len(datos.copy())
        lista_pesos = []
        lista_fechas = []

        for index in range(num_regis):
            fecha = datos[index][0]
            peso = datos[index][1]
            lista_fechas.append(fecha)
            lista_pesos.append(peso)
        
        lista_fechas.reverse()
        lista_pesos.reverse()

        fig, ax = plt.subplots()
        ax.plot(lista_fechas, lista_pesos, marker='o')

        ax.set_title("Evolutivo pesos por fecha")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Pesaje")

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        canvas.draw()

        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.canvas = canvas

    def actualizar_grafico(self):
        self.canvas.get_tk_widget().destroy()
        self.graficar()

    def insert_text(self):
        self.text.insert(self.ent7.get())


    def cerrar(self):
        root.quit()
        root.destroy()


    def consulta(self):
        book = self.trv.get_children()
        for element in book:
            self.trv.delete(element)
        query = 'SELECT * FROM control_pesos ORDER BY Fecha DESC'
        rows = app.lanza_querys(query)
        for row in rows:
            self.trv.insert('', 0, text=row[1],values=row)
        return query
    
    def chequeo(self):
        return len(self.ent1.get()) != 0 and len(self.ent2.get()) != 0 and len(self.ent3.get()) != 0 and len(self.ent4.get()) != 0 and len(self.ent5.get()) != 0 and len(self.ent6.get()) != 0 

    def filtrar(self):
        if self.chequeo:
            book = self.trv.get_children()
            for element in book:
                self.trv.delete(element)
            query = f'SELECT * FROM control_pesos WHERE Fecha > "{self.ent1.get()}" ORDER BY Fecha DESC'
            rows = app.lanza_querys(query)
            for row in rows:
                self.trv.insert('', 0, text=row[1],values=row)
            self.ent1.delete(0,END)
        else: 
            print('Filtro no aplicado')
            self.consulta()
    
    def agregar(self):
            if self.chequeo:
                fecha = self.ent1.get()
                try:
                    fecha = fecha.replace("/", "-")
                except:
                    pass
                if lectura_filas() == []:
                    fecha_reg_anterior = "NULL"
                    peso = float(self.ent2.get()) 
                    peso_ayer = 0
                else:
                    fecha_reg_anterior = lectura_filas()[-1][0]
                    peso = float(self.ent2.get())
                    peso_ayer = float(app.auxilia_consultas('Peso',fecha_reg_anterior)[0][0])
                estatura = int(170)
                MET_gym = float(6)
                MET_cardio = float(3.5)
                cardio = bool(self.ent4.get())
                tiempo_entreno = int(self.ent3.get())
                tiempo_cardio = int(self.ent5.get())
                edad = int(self.ent6.get())
                query = f"INSERT INTO control_pesos VALUES('{fecha}',{peso},{peso_ayer},{round(0, 2)}, {round(peso-peso_ayer,2)}, {round(0,2)}, {round(peso/(estatura/100),2)}, {round((((MET_gym*3.5*peso)/200)*tiempo_entreno),2)}, {cardio}, {round(tiempo_cardio*((MET_cardio*3.5*peso)/200),2)},{round((((MET_gym*3.5*peso)/200)*tiempo_entreno)+(tiempo_cardio*((MET_cardio*3.5*peso)/200))+((10*peso)+(6.25*estatura)-(5*(edad)+5)),2)})"
                app.lanza_querys(query)
                self.ent1.delete(0,END)
                self.ent2.delete(0,END)
                self.ent3.delete(0,END)
                self.ent4.delete(0,END)
                self.ent5.delete(0,END)
                self.ent6.delete(0,END)
                self.consulta()
            else:
                print('No se ha guardado')
                self.consulta()

    def eliminar(self): #Me falta crear un error cuando el resgitro no este en tabla
        if len(self.ent1.get()) != 0:
            fecha_borrado = self.ent1.get()
            try:
                query = f'DELETE FROM control_pesos WHERE Fecha = "{fecha_borrado}"'
                app.lanza_querys(query)
            except ValueError as error:
                print('Este registro no esta en la tabla')
            self.consulta()
    
    def actualizar(self):
        if len(self.ent1.get()) != 0 and (len(self.ent2.get()) != 0 or len(self.ent3.get()) != 0 or len(self.ent4.get()) != 0 or len(self.ent5.get()) != 0 or len(self.ent6.get()) != 0):
            query = f'UPDATE control_pesos SET ... WHERE Fecha = "{self.ent1.get()}"'
        #Dandole vueltas a crear una query con los campos que esten rellenos con for o con listas





if __name__ == '__main__':
    if os.path.exists(TABLA) == False:
        creacion_tabla()
        print(f"Se genero la tabla de datos en tu carpeta actual --> {os.getcwd()}")
    else:
        pass 
    root = Tk()
    pesos = Pesos(root)
    root.mainloop()
    

