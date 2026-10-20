# Sistema Distribuido de Gestion de Parqueadero

Sistema de control y visualizacion de parqueadero desarrollado en C++ y Python, utilizando sockets TCP/IP, programacion multihilo y librerias dinamicas (DLL) para la integracion entre modulos.

---

## Estructura del Repositorio

- generador_cpp/: Modulo cliente, generador automatico de vehiculos y listas enlazadas.
- receptor_dll_cpp/: Modulo servidor, sockets TCP, hilos y exportacion de libreria DLL.
- visualizador_python/: Modulo GUI, interfaz grafica en Tkinter y conexion mediante ctypes.

---

## Diagrama UML

![Diagrama UML](Diagrama_UML.png)

---

## Compilacion y Ejecucion

1. Compilar el Servidor y la DLL (C++):
g++ -shared -o visualizador_python/receptor.dll receptor_dll_cpp/NodoMensaje.cpp receptor_dll_cpp/ColaMensajes.cpp receptor_dll_cpp/ServidorSocket.cpp receptor_dll_cpp/dll_main.cpp -lws2_32 -static-libgcc -static-libstdc++ -Wl,-Bstatic -lstdc++ -lpthread -Wl,-Bdynamic

2. Compilar el Generador de Clientes (C++):
g++ -o generador_cpp/generador_app.exe generador_cpp/NodoVehiculo.cpp generador_cpp/ListaParqueadero.cpp generador_cpp/ClienteSocket.cpp generador_cpp/GeneradorPlacas.cpp generador_cpp/main.cpp -lws2_32 -static-libgcc -static-libstdc++ -Wl,-Bstatic -lstdc++ -lpthread -Wl,-Bdynamic

3. Ejecutar el Visualizador Grafico (Python):
python visualizador_python/main.py

4. Ejecutar el Generador (Cliente):
./generador_cpp/generador_app.exe
