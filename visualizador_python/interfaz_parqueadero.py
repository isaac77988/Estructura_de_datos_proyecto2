import tkinter as tk
from tkinter import messagebox
import socket
from datetime import datetime
from modelo_celda import ModeloCelda
from conector_dll import ConectorDLL

class InterfazParqueadero:
    def __init__(self, conector: ConectorDLL, total_celdas: int = 12):
        self.conector = conector
        self.total_celdas = total_celdas
        self.celdas = {i: ModeloCelda(i) for i in range(1, total_celdas + 1)}
        self.widgets_celdas = {}

        self.root = tk.Tk()
        self.root.title("Control de Parqueadero - C++ Sockets y DLL")
        self.root.geometry("920x640")
        self.root.configure(bg="#0f172a")
        self.root.minsize(820, 540)

        self._construir_interfaz()

    def _construir_interfaz(self):
        # Encabezado sobrio
        frame_header = tk.Frame(self.root, bg="#0f172a", pady=10)
        frame_header.pack(fill="x")

        lbl_titulo = tk.Label(
            frame_header,
            text="SISTEMA DE CONTROL DE PARQUEADERO",
            font=("Segoe UI", 16, "bold"),
            bg="#0f172a",
            fg="#f8fafc"
        )
        lbl_titulo.pack()

        texto_dll = (
            f"Estado del Servidor (Puerto {self.conector.puerto}): Conectado"
            if self.conector.activo
            else "Estado del Servidor: Desconectado"
        )
        color_dll = "#4ade80" if self.conector.activo else "#ef4444"

        self.lbl_estado_red = tk.Label(
            frame_header,
            text=texto_dll,
            font=("Segoe UI", 10),
            bg="#0f172a",
            fg=color_dll
        )
        self.lbl_estado_red.pack(pady=(2, 6))

        # Panel de control con botones separados de Ingreso y Salida
        frame_manual = tk.Frame(self.root, bg="#1e293b", padx=15, pady=8, relief="solid", bd=1)
        frame_manual.pack(fill="x", padx=25, pady=4)

        lbl_placa_m = tk.Label(frame_manual, text="Placa:", font=("Segoe UI", 9), bg="#1e293b", fg="#cbd5e1")
        lbl_placa_m.pack(side="left", padx=5)
        
        self.entry_placa = tk.Entry(frame_manual, font=("Consolas", 10), width=10, justify="center")
        self.entry_placa.pack(side="left", padx=5)
        self.entry_placa.insert(0, "ABC-123")

        lbl_celda_m = tk.Label(frame_manual, text="Celda (1-12):", font=("Segoe UI", 9), bg="#1e293b", fg="#cbd5e1")
        lbl_celda_m.pack(side="left", padx=5)

        self.entry_celda = tk.Entry(frame_manual, font=("Consolas", 10), width=5, justify="center")
        self.entry_celda.pack(side="left", padx=5)
        self.entry_celda.insert(0, "1")

        btn_ingreso = tk.Button(
            frame_manual,
            text="Dar Ingreso",
            font=("Segoe UI", 9, "bold"),
            bg="#059669",
            fg="#ffffff",
            activebackground="#047857",
            activeforeground="#ffffff",
            padx=10,
            pady=2,
            command=self._dar_ingreso
        )
        btn_ingreso.pack(side="left", padx=10)

        btn_salida = tk.Button(
            frame_manual,
            text="Dar Salida",
            font=("Segoe UI", 9, "bold"),
            bg="#b91c1c",
            fg="#ffffff",
            activebackground="#991b1b",
            activeforeground="#ffffff",
            padx=10,
            pady=2,
            command=self._dar_salida
        )
        btn_salida.pack(side="left", padx=5)

        # Contadores de celdas
        frame_contadores = tk.Frame(self.root, bg="#0f172a")
        frame_contadores.pack(pady=6)

        self.lbl_disponibles = tk.Label(
            frame_contadores,
            text=f"Disponibles: {self.total_celdas}",
            font=("Segoe UI", 10, "bold"),
            bg="#065f46",
            fg="#34d399",
            padx=12,
            pady=4
        )
        self.lbl_disponibles.pack(side="left", padx=6)

        self.lbl_ocupadas = tk.Label(
            frame_contadores,
            text="Ocupadas: 0",
            font=("Segoe UI", 10, "bold"),
            bg="#7f1d1d",
            fg="#fca5a5",
            padx=12,
            pady=4
        )
        self.lbl_ocupadas.pack(side="left", padx=6)

        # Cuadrícula de celdas
        contenedor_grid = tk.Frame(self.root, bg="#0f172a")
        contenedor_grid.pack(expand=True, fill="both", padx=25, pady=4)

        columnas = 4
        for i in range(1, self.total_celdas + 1):
            fila = (i - 1) // columnas
            col = (i - 1) % columnas

            frame_celda = tk.Frame(
                contenedor_grid,
                bg="#10b981",
                bd=1,
                relief="solid",
                padx=10,
                pady=8
            )
            frame_celda.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")
            contenedor_grid.grid_columnconfigure(col, weight=1)
            contenedor_grid.grid_rowconfigure(fila, weight=1)

            lbl_num = tk.Label(frame_celda, text=f"Celda {i}", font=("Segoe UI", 11, "bold"), bg="#10b981", fg="#ffffff")
            lbl_num.pack()

            lbl_estado = tk.Label(frame_celda, text="DISPONIBLE", font=("Segoe UI", 9, "bold"), bg="#059669", fg="#ffffff", padx=6, pady=2)
            lbl_estado.pack(pady=4)

            lbl_placa = tk.Label(frame_celda, text="---", font=("Consolas", 12, "bold"), bg="#10b981", fg="#ffffff")
            lbl_placa.pack(pady=2)

            lbl_hora = tk.Label(frame_celda, text="--:--:--", font=("Segoe UI", 8), bg="#10b981", fg="#ecfdf5")
            lbl_hora.pack()

            self.widgets_celdas[i] = {
                "frame": frame_celda,
                "lbl_num": lbl_num,
                "lbl_estado": lbl_estado,
                "lbl_placa": lbl_placa,
                "lbl_hora": lbl_hora
            }

        # Barra de registro inferior
        self.lbl_log = tk.Label(
            self.root,
            text="Sistema en espera de tramas...",
            font=("Consolas", 9),
            bg="#1e293b",
            fg="#94a3b8",
            pady=8
        )
        self.lbl_log.pack(fill="x", side="bottom")

    def _dar_ingreso(self):
        placa = self.entry_placa.get().strip().upper()
        celda_str = self.entry_celda.get().strip()

        if not placa or not celda_str.isdigit():
            messagebox.showerror("Error", "Ingrese una placa válida y un número de celda.")
            return

        num_celda = int(celda_str)
        if num_celda < 1 or num_celda > self.total_celdas:
            messagebox.showerror("Error", f"La celda debe estar entre 1 y {self.total_celdas}.")
            return

        # Validar si la celda ya está ocupada
        if self.celdas[num_celda].ocupada:
            messagebox.showwarning("Celda Ocupada", f"La Celda #{num_celda} ya se encuentra ocupada por el vehículo {self.celdas[num_celda].placa}.")
            return

        # Validar si la placa ya está registrada en otra celda
        for c_id, c_obj in self.celdas.items():
            if c_obj.placa == placa:
                messagebox.showwarning("Vehículo Registrado", f"El vehículo con placa {placa} ya se encuentra registrado en la Celda #{c_id}.")
                return

        hora_actual = datetime.now().strftime("%H:%M:%S")
        trama = f"{placa}|{hora_actual}|{num_celda}|OCUPAR"
        self._enviar_socket(trama)

    def _dar_salida(self):
        placa = self.entry_placa.get().strip().upper()
        celda_str = self.entry_celda.get().strip()

        if not placa and not celda_str.isdigit():
            messagebox.showerror("Error", "Ingrese la placa o el número de celda para dar salida.")
            return

        num_celda = -1
        # Buscar celda por placa o por número de celda directo
        if placa:
            for c_id, c_obj in self.celdas.items():
                if c_obj.placa == placa:
                    num_celda = c_id
                    break
        elif celda_str.isdigit():
            num_celda = int(celda_str)

        if num_celda == -1 or num_celda not in self.celdas or not self.celdas[num_celda].ocupada:
            messagebox.showerror("Error", "El vehículo o celda especificada no se encuentra ocupada actualmente.")
            return

        celda_obj = self.celdas[num_celda]
        placa_a_liberar = celda_obj.placa
        hora_actual = datetime.now().strftime("%H:%M:%S")

        trama = f"{placa_a_liberar}|{hora_actual}|{num_celda}|LIBERAR"
        self._enviar_socket(trama)

    def _enviar_socket(self, trama: str):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 8080))
            s.sendall(trama.encode("utf-8"))
            s.close()
        except Exception as e:
            messagebox.showwarning("Aviso", f"Error de conexión con el socket: {e}")

    def procesar_trama(self, trama: str):
        partes = trama.split("|")
        if len(partes) != 4:
            return

        placa, hora, celda_str, accion = partes
        try:
            num_celda = int(celda_str)
        except ValueError:
            return

        if num_celda not in self.celdas:
            return

        celda_obj = self.celdas[num_celda]
        if accion == "OCUPAR":
            celda_obj.ocupar(placa, hora)
            self.lbl_log.config(
                text=f"Entrada registrada: Vehículo {placa} en celda {num_celda} a las {hora}",
                fg="#f87171"
            )
        elif accion == "LIBERAR":
            celda_obj.liberar()
            self.lbl_log.config(
                text=f"Salida registrada: Vehículo {placa} liberó la celda {num_celda} a las {hora}",
                fg="#4ade80"
            )

        self._actualizar_widget_celda(num_celda)
        self._actualizar_contadores()

    def _actualizar_widget_celda(self, num_celda: int):
        celda_obj = self.celdas[num_celda]
        w = self.widgets_celdas[num_celda]

        if celda_obj.ocupada:
            bg_principal = "#ef4444"
            bg_badge = "#991b1b"
            texto_estado = "OCUPADA"
            texto_placa = celda_obj.placa
            texto_hora = celda_obj.hora_ingreso
        else:
            bg_principal = "#10b981"
            bg_badge = "#059669"
            texto_estado = "DISPONIBLE"
            texto_placa = "---"
            texto_hora = "--:--:--"

        w["frame"].config(bg=bg_principal)
        w["lbl_num"].config(bg=bg_principal)
        w["lbl_estado"].config(bg=bg_badge, text=texto_estado)
        w["lbl_placa"].config(bg=bg_principal, text=texto_placa)
        w["lbl_hora"].config(bg=bg_principal, text=texto_hora)

    def _actualizar_contadores(self):
        ocupadas = sum(1 for c in self.celdas.values() if c.ocupada)
        libres = self.total_celdas - ocupadas
        self.lbl_disponibles.config(text=f"Disponibles: {libres}")
        self.lbl_ocupadas.config(text=f"Ocupadas: {ocupadas}")

    def _bucle_escucha_dll(self):
        evento = self.conector.leer_evento()
        if evento:
            self.procesar_trama(evento)
        self.root.after(200, self._bucle_escucha_dll)

    def iniciar(self):
        def al_cerrar():
            self.conector.cerrar()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", al_cerrar)
        self.root.after(200, self._bucle_escucha_dll)
        self.root.mainloop()
