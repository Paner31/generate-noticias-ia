#!/bin/bash

# Script de instalación automática para Azure VM
# Ejecutar como: bash setup-azure.sh

set -e

echo "======================================"
echo "News Generator - Azure Deployment"
echo "======================================"
echo ""

# Actualizar sistema
echo "Actualizando sistema..."
sudo apt-get update
sudo apt-get upgrade -y

echo ""
echo "======================================"
echo "Instalando dependencias..."
echo "======================================"

# Instalar dependencias
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    software-properties-common

echo ""
echo "======================================"
echo "Instalando Docker..."
echo "======================================"

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh

# Agregar usuario actual al grupo docker
sudo usermod -aG docker $USER

echo ""
echo "======================================"
echo "Instalando Docker Compose..."
echo "======================================"

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo ""
echo "✓ Docker instalado correctamente!"
docker --version
docker-compose --version

echo ""
echo "======================================"
echo "Clonando repositorio..."
echo "======================================"
echo ""

# Pedir URL del repositorio
read -p "Ingresa la URL de tu repositorio GitHub: " REPO_URL

cd ~
git clone $REPO_URL
cd news-generator

echo ""
echo "✓ Repositorio clonado!"
echo ""
echo "======================================"
echo "Configurando variables de entorno..."
echo "======================================"

# Crear archivo .env para backend si no existe
if [ ! -f "backend/.env" ]; then
    echo "Creando backend/.env"
    cat > backend/.env << 'EOL'
# Configuración del backend
# IMPORTANTE: Reemplaza con tus credenciales reales

# OpenAI API Key
OPENAI_API_KEY=sk-tu-api-key-aqui

# Otras configuraciones (ajusta según necesites)
# DATABASE_URL=
# SECRET_KEY=
EOL
fi

echo ""
echo "⚠️  IMPORTANTE: Debes configurar las credenciales en backend/.env"
echo ""
echo "Abriendo editor nano..."
echo "Instrucciones:"
echo "  1. Reemplaza 'sk-tu-api-key-aqui' con tu API key real"
echo "  2. Guarda: Ctrl + O, presiona Enter"
echo "  3. Sal: Ctrl + X"
echo ""
read -p "Presiona ENTER para abrir el editor..."

nano ~/news-generator/backend/.env

echo ""
echo "======================================"
echo "Iniciando aplicación con Docker..."
echo "======================================"
echo ""

# Reiniciar sesión de grupo docker sin cerrar sesión
sg docker -c "docker-compose up -d"

echo ""
echo "Esperando que los contenedores inicien..."
sleep 5

echo ""
sg docker -c "docker-compose ps"

echo ""
echo "======================================"
echo "✓ ¡Despliegue completado exitosamente!"
echo "======================================"
echo ""

# Obtener IP pública de Azure
PUBLIC_IP=$(curl -s -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text" 2>/dev/null || echo "NO_DISPONIBLE")

if [ "$PUBLIC_IP" != "NO_DISPONIBLE" ]; then
    echo "🌐 Accede a tu aplicación:"
    echo "   Frontend: http://$PUBLIC_IP:3000"
    echo "   Backend:  http://$PUBLIC_IP:8000"
    echo "   Health:   http://$PUBLIC_IP:8000/health"
else
    echo "🌐 Accede a tu aplicación usando la IP pública de Azure:"
    echo "   Frontend: http://TU_IP_PUBLICA:3000"
    echo "   Backend:  http://TU_IP_PUBLICA:8000"
fi

echo ""
echo "📋 Comandos útiles:"
echo "   Ver logs:      cd ~/news-generator && docker-compose logs -f"
echo "   Reiniciar:     docker-compose restart"
echo "   Detener:       docker-compose down"
echo "   Ver estado:    docker-compose ps"
echo ""
echo "======================================"
