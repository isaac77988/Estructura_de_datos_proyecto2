import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from modelo_celda import ModeloCelda
from conector_dll import ConectorDLL

class InterfazParqueadero:
    """Gestiona la interfaz grafica del parqueadero y la sincronizacion con la libreria dinamica."""

    def _init_(self, conector: ConectorDLL, total_celdas: int = 12, puerto_web: int = 5000):
        self.conector = conector
        self.total_celdas = total_celdas
        self.puerto_web = puerto_web
        self.celdas = {i: ModeloCelda(i) for i in range(1, total_celdas + 1)}
        self.ultimo_log = "Esperando recepción de placas desde el socket C++..."
        self.ejecutando = True

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

        if accion == "OCUPAR":
            self.celdas[num_celda].ocupar(placa, hora)
            self.ultimo_log = f"[INGRESO] Placa {placa} ocupó la Celda #{num_celda} a las {hora}"
        elif accion == "LIBERAR":
            self.celdas[num_celda].liberar()
            self.ultimo_log = f"[SALIDA - PLACA REPETIDA] Vehículo {placa} liberó la Celda #{num_celda} a las {hora}"

    def _bucle_lectura_dll(self):
        while self.ejecutando:
            evento = self.conector.leer_evento()
            if evento:
                print(f"[DLL -> PYTHON] Evento capturado: {evento}")
                self.procesar_trama(evento)
            time.sleep(0.2)

    def obtener_estado_json(self) -> str:
        datos = {
            "dll_activa": self.conector.activo,
            "ultimo_log": self.ultimo_log,
            "celdas": [self.celdas[i].a_diccionario() for i in range(1, self.total_celdas + 1)]
        }
        return json.dumps(datos)

    def iniciar(self):
        hilo_dll = threading.Thread(target=self._bucle_lectura_dll, daemon=True)
        hilo_dll.start()

        app_ref = self

        class ManejadorWeb(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

            def do_GET(self):
                if self.path == "/api/estado":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(app_ref.obtener_estado_json().encode("utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(app_ref._generar_html().encode("utf-8"))

        servidor_http = HTTPServer(("0.0.0.0", self.puerto_web), ManejadorWeb)
        print("============================================================")
        print(f" VISUALIZADOR GRAFICO ACTIVO EN PUERTO WEB: {self.puerto_web}")
        print(f" Socket C++ (Libreria Dinamica) escuchando en puerto: {self.conector.puerto}")
        print("============================================================")
        try:
            servidor_http.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.ejecutando = False
            self.conector.cerrar()

    def _generar_html(self) -> str:
        return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Visualizador de Parqueadero - C++ Socket & DLL</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; text-align: center; }
        h1 { margin-bottom: 5px; color: #38bdf8; }
        .subtitulo { color: #94a3b8; margin-bottom: 15px; font-size: 14px; }
        .resumen { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; font-weight: bold; }
        .badge-libre { background: #065f46; color: #34d399; padding: 6px 14px; border-radius: 20px; }
        .badge-ocupada { background: #7f1d1d; color: #f87171; padding: 6px 14px; border-radius: 20px; }
        .log-box { background: #1e293b; border: 1px solid #334155; padding: 12px; border-radius: 8px; max-width: 900px; margin: 0 auto 20px auto; font-family: monospace; font-size: 15px; color: #fbbf24; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; max-width: 900px; margin: 0 auto; }
        .celda { padding: 18px; border-radius: 12px; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.4); }
        .libre { background: linear-gradient(135deg, #059669, #10b981); border: 2px solid #34d399; }
        .ocupada { background: linear-gradient(135deg, #b91c1c, #ef4444); border: 2px solid #f87171; transform: scale(1.02); }
        .num { font-size: 18px; font-weight: bold; margin-bottom: 6px; }
        .estado { font-size: 13px; font-weight: bold; letter-spacing: 1px; padding: 3px 8px; border-radius: 4px; background: rgba(0,0,0,0.25); display: inline-block; margin-bottom: 10px; }
        .placa { font-family: monospace; font-size: 20px; font-weight: bold; background: rgba(255,255,255,0.15); padding: 6px; border-radius: 6px; margin-bottom: 6px; }
        .hora { font-size: 13px; color: #e2e8f0; }
    </style>
</head>
<body>
    <h1>SISTEMA VISUALIZADOR DE PARQUEADERO</h1>
    <div class="subtitulo" id="estado-dll">Conectando con Librería Dinámica C++...</div>
    <div class="resumen">
        <span class="badge-libre" id="cont-libres">Disponibles: 12</span>
        <span class="badge-ocupada" id="cont-ocupadas">Ocupadas: 0</span>
    </div>
    <div class="log-box" id="log-evento">Esperando datos...</div>
    <div class="grid" id="contenedor-celdas"></div>

    <script>
        async function actualizar() {
            try {
                const res = await fetch('/api/estado');
                const data = await res.json();
                document.getElementById('estado-dll').innerText = data.dll_activa 
                    ? "🟢 Librería Dinámica C++ Activa (Escuchando Socket TCP en Puerto 8080)" 
                    : "🔴 Librería Dinámica no compilada o inactiva";
                document.getElementById('log-evento').innerText = data.ultimo_log;

                let libres = 0;
                let ocupadas = 0;
                const cont = document.getElementById('contenedor-celdas');
                cont.innerHTML = '';
                data.celdas.forEach(c => {
                    if (c.ocupada) ocupadas++; else libres++;
                    const div = document.createElement('div');
                    div.className = 'celda ' + (c.ocupada ? 'ocupada' : 'libre');
                    div.innerHTML = `
                        <div class="num">CELDA #${c.numero}</div>
                        <div class="estado">${c.ocupada ? 'OCUPADA' : 'DISPONIBLE'}</div>
                        <div class="placa">${c.ocupada ? c.placa : '---'}</div>
                        <div class="hora">Hora: ${c.ocupada ? c.hora : '--:--:--'}</div>
                    `;
                    cont.appendChild(div);
                });
                document.getElementById('cont-libres').innerText = Disponibles: ${libres};
                document.getElementById('cont-ocupadas').innerText = Ocupadas: ${ocupadas};
            } catch (e) {}
        }
        setInterval(actualizar, 400);
        actualizar();
    </script>
</body>
</html>"""
