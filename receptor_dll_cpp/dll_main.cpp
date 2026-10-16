#include "ServidorSocket.h"

#ifdef _WIN32
    #define EXPORTAR __declspec(dllexport)
#else
    #define EXPORTAR __attribute__((visibility("default")))
#endif

static ServidorSocket* servidor_global = nullptr;

extern "C" {

    EXPORTAR bool iniciar_servidor(int puerto) {
        if (servidor_global != nullptr) {
            delete servidor_global;
        }
        servidor_global = new ServidorSocket(puerto);
        return servidor_global->iniciar();
    }

    EXPORTAR const char* obtener_ultimo_evento() {
        if (servidor_global == nullptr) {
            return "";
        }
        return servidor_global->extraerSiguienteEvento();
    }

    EXPORTAR void detener_servidor() {
        if (servidor_global != nullptr) {
            servidor_global->detener();
            delete servidor_global;
            servidor_global = nullptr;
        }
    }

}
