# 📋 Comandos Útiles - Azure Deployment

## 🔑 Información del Servidor

**IP Pública:** `20.190.197.238`
**VM Name:** `Markup-Blog`
**Usuario:** `azureuser`
**Directorio del proyecto:** `~/generate-noticias-ia`

**URLs de acceso:**
- Frontend: http://20.190.197.238:3000
- Backend: http://20.190.197.238:8000
- Health Check: http://20.190.197.238:8000/health

---

## 🚀 Proceso Completo de Despliegue (Lo que hicimos)

### 1. Crear VM en Azure Portal
```
1. Portal Azure → Virtual Machines → Create
2. Configuración:
   - Name: Markup-Blog
   - Image: Ubuntu Server 22.04 LTS
   - Size: B1s (Free tier)
   - Authentication: SSH key
   - Key pair name: news-generator-key
3. Networking → Abrir puertos: 22, 3000, 8000
4. Create y descargar archivo .pem
```

### 2. Conectarse por SSH (desde Windows)
```cmd
REM Navegar a donde está el archivo .pem
cd Downloads

REM Conectar a la VM
ssh -i news-generator-key.pem azureuser@20.190.197.238
```

### 3. Instalar Docker y Docker Compose
```bash
# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependencias
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release git

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

### 4. Clonar Repositorio
```bash
cd ~
git clone https://github.com/Paner31/generate-noticias-ia.git
cd generate-noticias-ia
```

### 5. Configurar Variables de Entorno
```bash
# Editar archivo .env
nano backend/.env
```

**Contenido del .env:**
```env
PERPLEXITY_API_KEY=pplx-tu-clave-real-aqui
OPENROUTER_API_KEY=sk-or-v1-tu-clave-real-aqui
BACKEND_PORT=8000
FRONTEND_URL=http://20.190.197.238:3000
MAX_NOTES_PER_GENERATION=5
DEFAULT_MAX_TOKENS=8000
OPENROUTER_MODEL=z-ai/glm-4.6
```

**⚠️ IMPORTANTE:** No dejar espacios al inicio de las líneas

**Guardar en nano:**
- `Ctrl + O` → Guardar
- `Enter` → Confirmar
- `Ctrl + X` → Salir

### 6. Configurar docker-compose.yml para IP pública
```bash
nano docker-compose.yml
```

Cambiar en la sección frontend:
```yaml
args:
  - VITE_API_URL=http://20.190.197.238:8000
```

### 7. Iniciar Aplicación
```bash
# Primera vez (o después de salir y reconectar SSH)
docker-compose up -d --build

# Si ya corrió antes, solo reiniciar
docker-compose restart
```

---

## 📝 Comandos Básicos Diarios

### Conectarse al Servidor
```cmd
REM Desde Windows (PowerShell/CMD)
cd Downloads
ssh -i news-generator-key.pem azureuser@20.190.197.238
```

### Navegar al Proyecto
```bash
cd ~/generate-noticias-ia
```

### Ver Estado de Contenedores
```bash
# Ver todos los contenedores
docker-compose ps

# Ver contenedores corriendo (alternativa)
docker ps
```

### Ver Logs
```bash
# Logs de todos los servicios en tiempo real
sudo docker-compose logs -f

# Logs solo del backend
sudo docker-compose logs -f backend

# Logs solo del frontend
sudo docker-compose logs -f frontend

# Ver últimas 50 líneas
sudo docker-compose logs --tail=50 backend

# Ver últimas 100 líneas de todos
sudo docker-compose logs --tail=100

# Logs sin seguir (ver y salir)
sudo docker-compose logs backend
```

**Salir de logs:** `Ctrl + C`

### Reiniciar Servicios
```bash
# Reiniciar todo
sudo docker-compose restart

# Reiniciar solo backend
sudo docker-compose restart backend

# Reiniciar solo frontend
sudo docker-compose restart frontend
```

### Detener/Iniciar Aplicación
```bash
# Detener todo
sudo docker-compose down

# Iniciar todo
sudo docker-compose up -d

# Iniciar reconstruyendo (después de cambios en código)
sudo docker-compose up -d --build
```

---

## 🔧 Editar Configuración

### Cambiar API Keys
```bash
cd ~/generate-noticias-ia

# Editar .env
nano backend/.env

# Después de guardar, reiniciar backend
sudo docker-compose restart backend
```

### Actualizar Código desde GitHub
```bash
cd ~/generate-noticias-ia

# Traer últimos cambios
git pull

# Reconstruir y reiniciar
sudo docker-compose up -d --build

# O solo reconstruir un servicio específico
sudo docker-compose up -d --build backend
sudo docker-compose up -d --build frontend
```

### Ver Contenido de Archivos
```bash
# Ver archivo .env (primeras 10 líneas)
cat backend/.env | head -10

# Ver docker-compose.yml
cat docker-compose.yml

# Ver todo el .env
cat backend/.env
```

---

## 🐛 Troubleshooting

### Error: Permission Denied (Docker)
```bash
# Opción 1: Usar sudo temporalmente
sudo docker-compose ps

# Opción 2: Salir y reconectar SSH (recomendado)
exit
# Volver a conectar con SSH
```

### Ver Errores Específicos
```bash
# Ver errores del backend
sudo docker-compose logs --tail=100 backend | grep -i error

# Ver todos los logs del backend con errores
sudo docker-compose logs backend | grep -i "error\|exception\|traceback"
```

### Contenedor se Reinicia Constantemente
```bash
# Ver por qué falló
sudo docker-compose logs backend

# Verificar estado
sudo docker-compose ps

# Forzar recreación
sudo docker-compose up -d --force-recreate backend
```

### Sin Espacio en Disco
```bash
# Ver espacio disponible
df -h

# Limpiar imágenes y contenedores viejos
docker system prune -a

# Limpiar solo contenedores detenidos
docker container prune

# Limpiar solo imágenes sin usar
docker image prune -a
```

### Verificar IP Pública
```bash
# Obtener IP pública de la VM
curl ifconfig.me

# O alternativa
curl icanhazip.com
```

### Verificar Puertos Abiertos
```bash
# Ver qué está escuchando en puerto 8000
sudo netstat -tulpn | grep 8000

# Ver qué está escuchando en puerto 3000
sudo netstat -tulpn | grep 3000
```

---

## 📊 Monitoreo

### Ver Uso de Recursos
```bash
# CPU, RAM, uso de red en tiempo real
docker stats

# Ver solo un contenedor
docker stats news-generator-backend
```

### Ver Procesos Dentro del Contenedor
```bash
# Entrar al contenedor backend
docker exec -it news-generator-backend /bin/bash

# Dentro del contenedor:
ps aux
ls -la
exit  # Para salir
```

---

## 🔄 Actualizaciones Comunes

### Cambiar API Key de OpenRouter
```bash
nano backend/.env
# Cambiar: OPENROUTER_API_KEY=sk-or-v1-nueva-clave
# Ctrl+O, Enter, Ctrl+X
sudo docker-compose restart backend
```

### Cambiar Modelo de OpenRouter
```bash
nano backend/.env
# Cambiar: OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
# Ctrl+O, Enter, Ctrl+X
sudo docker-compose restart backend
```

### Aplicar Cambios de Código
```bash
cd ~/generate-noticias-ia
git pull
sudo docker-compose up -d --build
sudo docker-compose logs -f
```

---

## 💾 Backup y Restauración

### Hacer Backup del .env
```bash
# Copiar .env a backup
cp backend/.env backend/.env.backup

# Ver backups
ls -la backend/*.backup
```

### Restaurar .env
```bash
# Restaurar desde backup
cp backend/.env.backup backend/.env
sudo docker-compose restart backend
```

---

## 🛑 Apagar/Encender VM (Ahorrar Créditos)

### Desde Azure Portal
```
1. Ve a portal.azure.com
2. Virtual Machines → Markup-Blog
3. Click "Stop" (no se cobra mientras está detenida)
4. Para iniciar: Click "Start"
```

### Desde Azure CLI (si tienes instalado)
```bash
# Detener VM
az vm stop --resource-group news-generator-rg --name Markup-Blog

# Iniciar VM
az vm start --resource-group news-generator-rg --name Markup-Blog
```

---

## 📱 Acceso desde el Navegador

**Desarrollo/Testing:**
- Frontend: http://20.190.197.238:3000
- Backend API: http://20.190.197.238:8000
- Health: http://20.190.197.238:8000/health
- Docs API: http://20.190.197.238:8000/docs

---

## 🆘 Comandos de Emergencia

### Reiniciar Todo desde Cero
```bash
cd ~/generate-noticias-ia
sudo docker-compose down
sudo docker-compose up -d --build --force-recreate
sudo docker-compose logs -f
```

### Ver Todo lo que Está Pasando
```bash
# Terminal 1: Ver logs del backend
sudo docker-compose logs -f backend

# Terminal 2 (nueva conexión SSH): Ver logs del frontend
sudo docker-compose logs -f frontend

# Terminal 3: Ver recursos
docker stats
```

### Eliminar Todo y Empezar de Nuevo
```bash
cd ~
sudo docker-compose down
sudo rm -rf generate-noticias-ia
git clone https://github.com/Paner31/generate-noticias-ia.git
cd generate-noticias-ia
nano backend/.env  # Configurar de nuevo
sudo docker-compose up -d --build
```

---

## 📞 Información de Contacto

**GitHub Repo:** https://github.com/Paner31/generate-noticias-ia
**Azure Portal:** https://portal.azure.com

---

## 🎯 Checklist Rápido

```bash
# ¿La app está corriendo?
docker-compose ps

# ¿Hay errores?
sudo docker-compose logs --tail=50

# ¿Puedo acceder desde el navegador?
curl http://20.190.197.238:8000/health

# ¿Necesito actualizar código?
git pull && sudo docker-compose up -d --build

# ¿Cambié el .env?
sudo docker-compose restart backend
```

---

**Última actualización:** 19 de Noviembre, 2025
