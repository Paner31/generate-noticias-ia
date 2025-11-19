#!/bin/bash

# Script de instalación automática para EC2
# Ejecutar como: bash setup-ec2.sh

set -e

echo "======================================"
echo "Instalando Docker y Docker Compose..."
echo "======================================"

# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependencias
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario actual al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo ""
echo "======================================"
echo "Docker instalado correctamente!"
echo "======================================"
docker --version
docker-compose --version

echo ""
echo "======================================"
echo "Clonando repositorio..."
echo "======================================"

# Pedir URL del repositorio
read -p "Ingresa la URL de tu repositorio GitHub: " REPO_URL

cd ~
git clone $REPO_URL
cd news-generator

echo ""
echo "======================================"
echo "Configurando variables de entorno..."
echo "======================================"

# Crear archivo .env para backend
echo "Creando backend/.env"
cat > backend/.env << 'EOL'
# Configuración del backend
OPENAI_API_KEY=tu_api_key_aqui
# Agrega otras variables necesarias
EOL

echo ""
echo "IMPORTANTE: Edita el archivo backend/.env con tus credenciales reales"
echo "Comando: nano ~/news-generator/backend/.env"
echo ""
read -p "Presiona ENTER cuando hayas configurado el .env..."

echo ""
echo "======================================"
echo "Iniciando aplicación con Docker..."
echo "======================================"

# Necesitamos reiniciar sesión para que docker funcione sin sudo
# pero podemos usar newgrp como workaround
newgrp docker << END
docker-compose up -d
docker-compose ps
END

echo ""
echo "======================================"
echo "¡Despliegue completado!"
echo "======================================"
echo "Backend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo "Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):3000"
echo ""
echo "Para ver logs: docker-compose logs -f"
echo "Para detener: docker-compose down"
echo "======================================"
