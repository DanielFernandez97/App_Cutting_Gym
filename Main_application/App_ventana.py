from tkinter import ttk
from tkinter import *
from tkinter import Text

import sys
import os
from dotenv import load_dotenv

load_dotenv()
INITIAL_PATH = os.getenv("INITIAL_PATH")
REPO_GYM_CUT = os.getenv("FOLDER_NAME")

ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(str(INITIAL_PATH), str(REPO_GYM_CUT)))


from Chatbot_model_from_scratch.chatbot_gym import *
from Chatbot_model_pretrained.Chatbot_pretrained import *

import os


import sqlite3 as sql
import AppDefi_SQL as app
from AppDefi_SQL import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#TODO
# Pasar variables al ingles


#Futuros desarrollos
#Incluir fotografia y comentario con IA sobre la evolucion del fisico, se necesitaran labelframe mas, necesitariamos dataset con los label
#Incluir un chatbot de un modelo desde 0 donde el usuario pueda preguntar cosas sobre el gym puede ser modelo fine tuned con info gym


TABLE = 'Cutting_table.db'
DIALOGUE_LIST = []

def add_placeholder(entry, placeholder):
    # Añadir el texto por defecto al Entry
    entry.insert(0, placeholder)
    entry.config(fg="#D3D3D3")  # Estilo visual para diferenciar el placeholder

    # Función que elimina el placeholder cuando el usuario hace clic
    def on_focus_in():
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.config(fg="black")  # Cambia el color al escribir texto

    # Función que restaura el placeholder si el usuario deja el campo vacío
    def on_focus_out():
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#D3D3D3")

    # Asignar los eventos
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

class Pesos:

    def __init__(self,root):

        self.estatura = int(170)
        self.MET_gym = float(6)
        self.MET_cardio = float(3.5)

        self.wind = root
        self.wind.title('Gym Cutting App')
        self.wind.geometry("1750x1150")

        frame1 = LabelFrame(self.wind, text='Weight by Date data', font=("Helvetica", 14)) 

        frame2 = LabelFrame(self.wind, text='Weight filtered', font=("Helvetica", 14))

        frame3 = LabelFrame(self.wind, text='Graphics', font=("Helvetica", 14))
        self.frame3 = frame3

        frame4 = LabelFrame(self.wind, text='Gym Chatbot', font=("Helvetica", 14))

        frame1.place(x=100,y=10, width=1600)
        frame2.place(x=100, y=280, width=750)
        frame3.place(x=900, y=280, width=800, height=793)
        frame4.place(x=100, y=600, width=750)

        self.trv = ttk.Treeview(frame1, columns= (1,2,3,4,5,6,7,8,9,10,11), show='headings', height=10)
        self.trv.grid()

        columnas = app.nombre_columnas()
        for numero, encabezado in enumerate(columnas):
            self.trv.heading(numero+1,text=list(encabezado))
            if len(encabezado[0]) > 18:
                anchura = 200
            else:
                anchura = 110
            self.trv.column(numero+1, width=anchura)
        self.consulta()

        self.text = Text(frame4, background="white", width=90, height=25)
        self.text.config(state="normal")
        self.text.grid()


        lbl1 = Label(frame2, text='Weighing Date', width= 20)
        lbl1.grid(row=0, padx=8, pady=5)
        self.ent1 = Entry(frame2)
        self.ent1.grid(row=0, column=1, padx=8, pady=5)
        add_placeholder(entry=self.ent1, placeholder="XX/MM/YYYY")

        lbl2 = Label(frame2, width= 20)
        lbl2.grid(row=1, padx=8, pady=5)

        lbl3 = Label(frame2, text='Weight', width= 20)
        lbl3.grid(row=1, padx=8, pady=5)
        self.ent2 = Entry(frame2)
        self.ent2.grid(row=1, column=1, padx=8, pady=5)
        add_placeholder(entry=self.ent2, placeholder="xx.xx")

        lbl4 = Label(frame2, width= 20)
        lbl4.grid(row=2, padx=8, pady=5)

        lbl5 = Label(frame2, text='Training Time', width= 20)
        lbl5.grid(row=2, padx=8, pady=5)
        self.ent3 = Entry(frame2)
        self.ent3.grid(row=2, column=1, padx=8, pady=5)
        add_placeholder(entry=self.ent3, placeholder="xx.xx")

        lbl6 = Label(frame2, width= 20)
        lbl6.grid(row=3, padx=8, pady=5)

        lbl7 = Label(frame2, text='Cardio 0/1', width= 20)
        lbl7.grid(row=3, padx=8, pady=5)
        self.ent4 = Entry(frame2)
        self.ent4.grid(row=3, column=1, padx=8, pady=5)
        add_placeholder(entry=self.ent4, placeholder="0/1 values only")

        lbl8 = Label(frame2, width= 20)
        lbl8.grid(row=4, padx=8, pady=5)

        lbl9 = Label(frame2, text='Cardio Time', width= 20)
        lbl9.grid(row=4, padx=8, pady=5)
        self.ent5 = Entry(frame2)
        self.ent5.grid(row=4, column=1, padx=8, pady=5)
        add_placeholder(entry=self.ent5, placeholder="xx.xx")

        lbl10 = Label(frame2, width= 20)
        lbl10.grid(row=5, padx=8, pady=5)

        lbl11 = Label(frame2, text='Age', width= 20)
        lbl11.grid(row=5, padx=8, pady=5)
        self.ent6 = Entry(frame2)
        self.ent6.grid(row=5, column=1, padx=8, pady=5)
        add_placeholder(entry=self.ent6, placeholder="Only integers")

        lbl12 = Label(frame2, width= 20)
        lbl12.grid(row=6, padx=8, pady=5)

        btt1 = Button(frame2, text='Add',command=self.agregar, width=12, height=2)
        btt1.grid(row=0, column=4)

        btt2 = Button(frame2, text='Filter', command=self.filtrar, width=12, height=2)
        btt2.grid(row=0, column=5)

        btt3 = Button(frame2, text='Update',command=self.actualizar, width=12, height=2)
        btt3.grid(row=1, column=4)

        btt4 = Button(frame2, text='Delete',command=self.eliminar, width=12, height=2)
        btt4.grid(row=1, column=5)

        btt5 = Button(master=frame3,text="Close",bg="red",command=self.cerrar, width=10, height=3, font=15)
        btt5.pack(side=BOTTOM)

        self.drop_list = ttk.Combobox(frame3, values=["Cardio Calories", "Weight", "Total Calories Burnt"], state="readonly")
        self.drop_list.set("Select the measure to plot")
        self.drop_list.pack(side=TOP,expand=YES, fill="x")

        btt6 = Button(master=frame3,text="Update Graphic",command=self.actualizar_grafico, width=12, height=2)
        btt6.pack(side=TOP,expand=YES, fill="x")


        self.ent7 = Entry(frame4)
        self.ent7.place(x=10, y=415, width=250)
        btt8 = Button(master=frame4,text="Ask Chatbot", command=self.chatbot_dialogue, width=15, height=2)
        btt8.grid()
        btt9 = Button(master=frame4,text="Clean Console", command=self.clean_console, width=15, height=2)
        btt9.place(x=450, y=405)

        self.graficar()

    def get_selection(self):
        selection = self.drop_list.get()
        return selection
  
    def graficar(self):
            
        datos = lectura_filas()
        num_regis = len(datos.copy())
        lista_x = []
        lista_y = []

        for index in range(num_regis):
            y = datos[index][0]
            x = datos[index][1] 
            lista_y.append(y)
            lista_x.append(x)
        
        lista_y.reverse()
        lista_x.reverse()

        fig, ax = plt.subplots()
        ax.plot(lista_y, lista_x, marker='o')
        ax.set_title(f"Weight Evolution by Date")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Weight")           

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        canvas.draw()

        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.canvas = canvas

    def clean_console(self):
        self.text.delete("1.0", END)  

    def actualizar_grafico(self):
        self.canvas.get_tk_widget().destroy()
        try: 
            self.label_text.destroy()
        except: 
            pass
        

        datos = lectura_filas()
        num_regis = len(datos.copy())
        lista_x = []
        lista_y = []

        for index in range(num_regis):
            y = datos[index][0] 
            if self.get_selection().lower() == "weight":
                x = datos[index][1]
            elif self.get_selection().lower() == "cardio calories":
                x = datos[index][9]
            elif self.get_selection().lower() == "total calories burnt":
                x = datos[index][10]
            else: 
                #Imprimir un texto por pantalla para que el usuario vea que no eligio la medida a graficar
                text = "There was an error in the measure chosen, select other measure and update the graph" 
                self.label_text = ttk.Label(self.frame3, text=text, font=25, justify="center")
                self.label_text.pack()
                return ""
            lista_y.append(y)
            lista_x.append(x)
        
        lista_y.reverse()
        lista_x.reverse()

        fig, ax = plt.subplots()
        ax.plot(lista_y, lista_x, marker='o')

        ax.set_title(f"{self.drop_list.selection_get()} Evolution by Date")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"{self.drop_list.selection_get().lower()}")       

        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        canvas.draw()

        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.canvas = canvas

    def chatbot_dialogue(self):
        
        user_question = str("User: ") + self.ent7.get() + "\n" 
        self.text.insert(INSERT, user_question)
        DIALOGUE_LIST.append(self.ent7.get())
        input = self.ent7.get()
        print(input)
        self.ent7.delete(0, END)
        response = get_response_LLM_pretrained(input_sentence=input)
        print(response)
        if "?" in response:
            cleaned_response = response.split("?",1)[1].lstrip().capitalize()
        else: 
            cleaned_response = response.lstrip().capitalize()
        #cleaned_response = response.split(input.split()[-1],1)[1].lstrip().capitalize()
        chatbot_response = str("Chatbot: ") + cleaned_response + "\n" 

        self.text.insert(INSERT, chatbot_response)


    def cerrar(self):
        root.quit()
        root.destroy()


    def consulta(self):
        book = self.trv.get_children()
        for element in book:
            self.trv.delete(element)
        query = 'SELECT * FROM weight_control ORDER BY Date DESC'
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
            query = f'SELECT * FROM weight_control WHERE Date > "{self.ent1.get()}" ORDER BY Date DESC'
            rows = app.lanza_querys(query)
            for row in rows:
                self.trv.insert('', 0, text=row[1],values=row)
            self.ent1.delete(0,END)
        else: 
            print('The filter was not applied')
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
                    peso_ayer = float(app.auxilia_consultas('Weight',fecha_reg_anterior)[0][0])
                cardio = bool(self.ent4.get())
                tiempo_entreno = int(self.ent3.get())
                tiempo_cardio = int(self.ent5.get())
                edad = int(self.ent6.get())
                query = f"INSERT INTO weight_control VALUES('{fecha}',{peso},{peso_ayer},{round(0, 2)}, {round(peso-peso_ayer,2)}, {round(0,2)}, {round(peso/(self.estatura/100),2)}, {round((((self.MET_gym*3.5*peso)/200)*tiempo_entreno),2)}, {cardio}, {round(tiempo_cardio*((self.MET_cardio*3.5*peso)/200),2)},{round((((self.MET_gym*3.5*peso)/200)*tiempo_entreno)+(tiempo_cardio*((self.MET_cardio*3.5*peso)/200))+((10*peso)+(6.25*self.estatura)-(5*(edad)+5)),2)})"
                app.lanza_querys(query)
                self.ent1.delete(0,END)
                self.ent2.delete(0,END)
                self.ent3.delete(0,END)
                self.ent4.delete(0,END)
                self.ent5.delete(0,END)
                self.ent6.delete(0,END)
                self.consulta()
            else:
                print('It was not saved')
                self.consulta()

    def eliminar(self): #Me falta crear un error cuando el resgitro no este en tabla
        if len(self.ent1.get()) != 0:
            fecha_borrado = self.ent1.get()
            try:
                query = f'DELETE FROM weight_control WHERE Date = "{fecha_borrado}"'
                app.lanza_querys(query)
            except ValueError as error:
                print('This record it is not on the table')
            self.ent1.delete(0,END)
            self.consulta()
    
    def actualizar(self):
        if len(self.ent1.get()) != 0 and (len(self.ent2.get()) != 0 or len(self.ent3.get()) != 0 or len(self.ent4.get()) != 0 or len(self.ent5.get()) != 0 or len(self.ent6.get()) != 0):
            lista_nombre_columnas = app.nombre_columnas()
            fecha_actualizar = self.ent1.get() 
            peso_ayer = float(app.auxilia_consultas('Weight',fecha_actualizar)[0][0])
            query = f'UPDATE weight_control SET {lista_nombre_columnas[0]} = "{self.ent1.get()}",{lista_nombre_columnas[1]} = {self.ent2.get()},{lista_nombre_columnas[2]} = {peso_ayer},{lista_nombre_columnas[3]} = {round(0,2)},{lista_nombre_columnas[4]} = {round(float(self.ent2.get()) - peso_ayer,2)},{lista_nombre_columnas[5]} = {round(0,2)},{lista_nombre_columnas[6]} = {round(float(self.ent2.get())/(float(self.estatura)/100),2)},{lista_nombre_columnas[7]} = {round((((self.MET_gym*3.5*float(self.ent2.get()))/200)*float(self.ent3.get())),2)},{lista_nombre_columnas[8]} = {int(self.ent4.get())},{lista_nombre_columnas[9]} = {round(float(self.ent5.get())*((self.MET_cardio*3.5*float(self.ent2.get()))/200),2)},{lista_nombre_columnas[10]} = {round((((self.MET_gym*3.5*float(self.ent2.get()))/200)*float(self.ent3.get()))+(float(self.ent5.get())*((self.MET_cardio*3.5*float(self.ent2.get()))/200))+((10*float(self.ent2.get()))+(6.25*self.estatura)-(5*(float(self.ent6.get()))+5)),2)} WHERE Fecha = "{self.ent1.get()}"'
            query = query.replace("(","").replace(",)","")

            try:
                app.lanza_querys(query)
            except ValueError as error:
                print('This record it is not on the table')
                self.consulta()
            
            self.ent1.delete(0,END)
            self.ent2.delete(0,END)
            self.ent3.delete(0,END)
            self.ent4.delete(0,END)
            self.ent5.delete(0,END)
            self.ent6.delete(0,END)
            self.consulta()


if __name__ == '__main__':
    if os.path.exists(TABLE) == False:
        creacion_tabla()
        print(f"The datatable was created on this path in you FileSystem --> {os.getcwd()}")

    root = Tk()
    pesos = Pesos(root)

    root.mainloop()
    

