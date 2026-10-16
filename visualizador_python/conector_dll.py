import ctypes
import os
import platform

class ConectorDLL:
    """Encapsula la carga de la libreria dinamica C++ (.dll en Windows / .so en Linux)."""

    def _init_(self, directorio_base: str, puerto: int = 8080):
        self.directorio_base = directorio_base
        self.puerto = puerto
        self.dll = None
        self.activo = False
        self.ruta_libreria = self._resolver_ruta_libreria()

    def _resolver_ruta_libreria(self) -> str:
        if platform.system() == "Windows":
            return os.path.join(self.directorio_base, "receptor.dll")
        return os.path.join(self.directorio_base, "lib_receptor.so")

    def inicializar(self) -> bool:
        if not os.path.exists(self.ruta_libreria):
            print(f"[AVISO] No se encontro la libreria dinamica en: {self.ruta_libreria}")
            return False

        try:
            self.dll = ctypes.CDLL(self.ruta_libreria)

            self.dll.iniciar_servidor.argtypes = [ctypes.c_int]
            self.dll.iniciar_servidor.restype = ctypes.c_bool

            self.dll.obtener_ultimo_evento.argtypes = []
            self.dll.obtener_ultimo_evento.restype = ctypes.c_char_p

            self.dll.detener_servidor.argtypes = []
            self.dll.detener_servidor.restype = None

            self.activo = self.dll.iniciar_servidor(self.puerto)
            return self.activo
        except Exception as e:
            print(f"[ERROR DLL] Fallo al cargar libreria dinamica: {e}")
            return False

    def leer_evento(self) -> str:
        if not self.activo or not self.dll:
            return ""
        datos = self.dll.obtener_ultimo_evento()
        if datos:
            return datos.decode("utf-8", errors="ignore").strip()
        return ""

    def cerrar(self):
        if self.activo and self.dll:
            self.dll.detener_servidor()
            self.activo = False
