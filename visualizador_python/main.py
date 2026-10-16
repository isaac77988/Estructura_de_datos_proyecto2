import os
from conector_dll import ConectorDLL
from interfaz_parqueadero import InterfazParqueadero

def main():
    ruta_base = os.path.dirname(os.path.abspath(__file__))

    # 1. Inicializar la libreria dinamica C++ (receptor.dll en Windows / lib_receptor.so en Linux)
    conector = ConectorDLL(directorio_base=ruta_base, puerto=8080)
    conector.inicializar()

    # 2. Iniciar la ventana grafica nativa de Tkinter
    app = InterfazParqueadero(conector=conector, total_celdas=12)
    app.iniciar()

if __name__ == "__main__":
    main()
