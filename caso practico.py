import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

class Sensor:
    def __init__(self):
        self.temperatura = 0
        self.humedad = 0
        self.running = True

    def leer_datos(self):
        while self.running:
            try:
                self.temperatura = random.uniform(0, 50)
                self.humedad = random.uniform(20, 90)
                if self.temperatura < 0 or self.humedad < 0:
                    raise ValueError("Valores inválidos del sensor")
            except ValueError as e:
                print(f"Error: {e}")
            finally:
                time.sleep(2)

class Interfaz:
    def __init__(self, root, sensor):
        self.sensor = sensor
        self.root = root
        self.root.title("Monitoreo de Sensor")
        self.root.geometry("400x300")
        self.root.config(bg="#e6f0ff")
        
        frame = tk.Frame(root, bg="#fff9cc", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        frame.pack(pady=20)
        
        self.label_temp = tk.Label(frame, text="Temperatura: -- °C", font=("Arial", 14), bg="#ffffff")
        self.label_temp.pack(pady=5)
        
        self.label_hum = tk.Label(frame, text="Humedad: -- %", font=("Arial", 14), bg="#ffffff")
        self.label_hum.pack(pady=5)
        
        self.entry_umbral = tk.Entry(frame, font=("Arial", 12), justify="center")
        self.entry_umbral.pack(pady=5)
        
        self.boton_confirmar = tk.Button(frame, text="Establecer Umbral", font=("Arial", 12, "bold"), bg="#ADD8E6", fg="white", command=self.verificar_umbral)
        self.boton_confirmar.pack(pady=5)
        
        self.label_estado = tk.Label(frame, text="Estado: Estable", font=("Arial", 14, "bold"), bg="#ccffcc", fg="white", padx=10, pady=5)
        self.label_estado.pack(pady=10, fill=tk.X)
        
        self.actualizar_datos()
    
    def actualizar_datos(self):
        self.label_temp.config(text=f"Temperatura: {self.sensor.temperatura:.2f} °C")
        self.label_hum.config(text=f"Humedad: {self.sensor.humedad:.2f} %")
        self.root.after(2000, self.actualizar_datos)
    
    def verificar_umbral(self):
        try:
            umbral = float(self.entry_umbral.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido")
        else:
            if self.sensor.temperatura > umbral:
                self.label_estado.config(text="Estado: Alerta", bg="red")
            else:
                self.label_estado.config(text="Estado: Normal", bg="green")
        finally:
            print("Verificación de umbral completada")

if __name__ == "__main__":
    sensor = Sensor()
    hilo_sensor = threading.Thread(target=sensor.leer_datos, daemon=True)
    hilo_sensor.start()
    
    root = tk.Tk()
    app = Interfaz(root, sensor)
    root.mainloop()
    
    sensor.running = False
