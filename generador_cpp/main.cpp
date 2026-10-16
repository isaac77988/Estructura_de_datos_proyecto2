#include "GeneradorPlacas.h"

int main() {
    // Conecta al servidor socket en 127.0.0.1 puerto 8080 con un parqueadero de 12 celdas
    GeneradorPlacas app_generador("127.0.0.1", 8080, 12);
    app_generador.ejecutarCicloContinuo();
    return 0;
}
