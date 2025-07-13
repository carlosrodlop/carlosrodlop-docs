#!/bin/bash

# Script de ayuda para ejecutar el generador de mapas de Portugal 2025
# Uso: ./run.sh [comando]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_help() {
    echo -e "${GREEN}Generador de Mapa de Ruta Portugal 2025${NC}"
    echo ""
    echo "Comandos disponibles:"
    echo "  build         - Construir la imagen Docker"
    echo "  run           - Ejecutar el generador de mapas"
    echo "  server        - Iniciar servidor web para ver los mapas"
    echo "  clean         - Limpiar contenedores e imágenes"
    echo "  shell         - Abrir shell interactivo en el contenedor"
    echo "  logs          - Ver logs del contenedor"
    echo "  help          - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./run.sh build"
    echo "  ./run.sh run"
    echo "  ./run.sh server"
}

build_image() {
    echo -e "${YELLOW}Construyendo imagen Docker...${NC}"
    docker-compose build portugal-map-generator
    echo -e "${GREEN}✓ Imagen construida exitosamente${NC}"
}

run_generator() {
    echo -e "${YELLOW}Ejecutando generador de mapas...${NC}"
    
    # Crear directorio de salida si no existe
    mkdir -p output
    
    # Ejecutar el contenedor
    docker-compose run --rm portugal-map-generator
    
    echo -e "${GREEN}✓ Mapa generado exitosamente${NC}"
    echo -e "Archivo guardado en: ${SCRIPT_DIR}/portugal_route_map.png"
}

start_server() {
    echo -e "${YELLOW}Iniciando servidor web...${NC}"
    docker-compose up -d map-server
    echo -e "${GREEN}✓ Servidor iniciado en http://localhost:8000${NC}"
    echo "Para detener el servidor: docker-compose down"
}

clean_containers() {
    echo -e "${YELLOW}Limpiando contenedores e imágenes...${NC}"
    docker-compose down --rmi all --volumes --remove-orphans
    echo -e "${GREEN}✓ Limpieza completada${NC}"
}

open_shell() {
    echo -e "${YELLOW}Abriendo shell interactivo...${NC}"
    docker-compose run --rm portugal-map-generator bash
}

show_logs() {
    docker-compose logs -f portugal-map-generator
}

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker no está instalado${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose no está instalado${NC}"
    exit 1
fi

# Procesar comando
case "${1:-help}" in
    build)
        build_image
        ;;
    run)
        build_image
        run_generator
        ;;
    server)
        build_image
        start_server
        ;;
    clean)
        clean_containers
        ;;
    shell)
        build_image
        open_shell
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        echo -e "${RED}Error: Comando desconocido '${1}'${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac
