import os
from conector_dll import ConectorDLL
from interfaz_parqueadero import InterfazParqueadero

def main():
    ruta_base = os.path.dirname(os.path.abspath(_file_))
    
    # 1. Inicializar la libreria dinamica C++ que escucha el socket en el puerto 8080
    conector = ConectorDLL(directorio_base=ruta_base, puerto=8080)
    conector.inicializar()

    # 2. Lanzar la interfaz grafica en el puerto 5000
    interfaz = InterfazParqueadero(conector=conector, total_celdas=12, puerto_web=5000)
    interfaz.iniciar()

if _name_ == "_main_":
    main()
