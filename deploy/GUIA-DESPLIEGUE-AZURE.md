# Guía de Despliegue en Azure

## 🎯 Resumen

Esta guía te ayudará a desplegar tu aplicación News Generator en Azure usando una Máquina Virtual (VM) con Docker.

**Beneficios de Azure:**
- ✅ $200 USD en créditos por 30 días
- ✅ 12 meses de servicios gratuitos
- ✅ B1s VM gratis durante 12 meses (750 horas/mes)

---

## Paso 1: Crear Máquina Virtual en Azure

### 1.1 Acceder al Portal de Azure
1. Ve a [portal.azure.com](https://portal.azure.com)
2. Inicia sesión con tu cuenta

### 1.2 Crear la VM
1. En el buscador superior, escribe "Virtual Machines" y selecciónalo
2. Click en **"+ Create"** → **"Azure virtual machine"**

### 1.3 Configuración Básica

**Pestaña "Basics":**

| Campo | Valor |
|-------|-------|
| **Subscription** | Tu suscripción (Azure subscription 1) |
| **Resource group** | Click "Create new" → Nombre: `news-generator-rg` |
| **Virtual machine name** | `news-generator-vm` |
| **Region** | Elige la más cercana (ej: East US, West Europe) |
| **Availability options** | No infrastructure redundancy required |
| **Security type** | Standard |
| **Image** | Ubuntu Server 22.04 LTS - x64 Gen2 |
| **Size** | **B1s** (1 vcpu, 1 GiB RAM) - **Free tier eligible** |

**Authentication:**
- **Authentication type:** SSH public key
- **Username:** `azureuser`
- **SSH public key source:** Generate new key pair
- **Key pair name:** `news-generator-key`

⚠️ **IMPORTANTE:** Cuando hagas click en "Review + create", Azure te pedirá descargar la clave privada (archivo .pem). **¡Guárdala en un lugar seguro!**

### 1.4 Configurar Puertos (Networking)

Click en la pestaña **"Networking"**:

1. **NIC network security group:** Advanced
2. Click **"Create new"** en Configure network security group

3. Agrega las siguientes reglas (click "+ Add an inbound rule" para cada una):

**Regla 1: SSH**
- Source: Any
- Source port ranges: *
- Destination: Any
- Service: SSH
- Destination port ranges: 22
- Protocol: TCP
- Action: Allow
- Priority: 100
- Name: `SSH`

**Regla 2: Frontend**
- Source: Any
- Source port ranges: *
- Destination: Any
- Service: Custom
- Destination port ranges: 3000
- Protocol: TCP
- Action: Allow
- Priority: 110
- Name: `Frontend`

**Regla 3: Backend**
- Source: Any
- Source port ranges: *
- Destination: Any
- Service: Custom
- Destination port ranges: 8000
- Protocol: TCP
- Action: Allow
- Priority: 120
- Name: `Backend`

4. Click **"OK"**

### 1.5 Crear la VM

1. Click **"Review + create"**
2. Espera la validación (debe decir "Validation passed")
3. Click **"Create"**
4. **Descarga la clave privada** (.pem file) cuando se te solicite
5. Espera 2-3 minutos mientras se crea la VM

---

## Paso 2: Obtener IP Pública

1. Una vez creada, click en **"Go to resource"**
2. En la página de la VM, busca **"Public IP address"** (ejemplo: 20.123.45.67)
3. **Copia esta IP** - la necesitarás para conectarte

---

## Paso 3: Conectar por SSH

### En Windows (PowerShell, CMD o Git Bash):

```bash
# Navega a donde descargaste el archivo .pem
cd Downloads

# Conecta a la VM (reemplaza con tu IP)
ssh -i news-generator-key.pem azureuser@TU_IP_PUBLICA
```

**Ejemplo:**
```bash
ssh -i news-generator-key.pem azureuser@20.123.45.67
```

**Si da error de permisos en Windows:**
- Usa Git Bash o WSL
- O ignora el warning y escribe "yes" cuando pregunte

### En Linux/Mac:

```bash
# Dar permisos correctos al archivo
chmod 400 ~/Downloads/news-generator-key.pem

# Conectar
ssh -i ~/Downloads/news-generator-key.pem azureuser@TU_IP_PUBLICA
```

✅ Deberías ver algo como: `azureuser@news-generator-vm:~$`

---

## Paso 4: Ejecutar Script de Instalación

Una vez conectado por SSH a tu VM de Azure:

```bash
# Descargar el script de instalación
curl -o setup-azure.sh https://raw.githubusercontent.com/TU_USUARIO/news-generator/main/deploy/setup-azure.sh

# Dar permisos de ejecución
chmod +x setup-azure.sh

# Ejecutar el script
bash setup-azure.sh
```

**El script hará automáticamente:**
1. ✓ Actualizar el sistema
2. ✓ Instalar Docker y Docker Compose
3. ✓ Clonar tu repositorio de GitHub
4. ✓ Crear archivo `.env`
5. ✓ Iniciar los contenedores

---

## Paso 5: Configurar Variables de Entorno

Durante la ejecución, el script abrirá el editor `nano` para que configures tus credenciales:

```env
# Reemplaza con tu API key real de OpenAI
OPENAI_API_KEY=sk-tu-clave-real-aqui

# Agrega otras variables si necesitas
```

**Guardar:**
1. Presiona `Ctrl + O`
2. Presiona `Enter`
3. Presiona `Ctrl + X` para salir

---

## Paso 6: Verificar Despliegue

### 6.1 En tu navegador:

Visita las siguientes URLs (reemplaza con tu IP):

- **Frontend:** `http://TU_IP_PUBLICA:3000`
- **Backend API Health:** `http://TU_IP_PUBLICA:8000/health`

### 6.2 Verificar contenedores en SSH:

```bash
# Ver estado de contenedores
cd ~/news-generator
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo del backend
docker-compose logs -f backend

# Ver logs solo del frontend
docker-compose logs -f frontend
```

---

## Comandos Útiles

```bash
# Ver contenedores corriendo
docker-compose ps

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Iniciar nuevamente
docker-compose up -d

# Reconstruir y reiniciar
docker-compose up -d --build

# Ver uso de recursos
docker stats

# Actualizar código desde GitHub
cd ~/news-generator
git pull
docker-compose up -d --build

# Ver IP pública desde dentro de la VM
curl -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text"
```

---

## Solución de Problemas

### ❌ No puedo acceder a http://IP:3000

**Posibles causas:**

1. **Firewall (NSG) no configurado:**
   - Ve a Azure Portal → Tu VM → Networking
   - Verifica que existan reglas para puertos 3000 y 8000

2. **Contenedores no están corriendo:**
   ```bash
   docker-compose ps
   # Si no están UP, revisa logs
   docker-compose logs
   ```

3. **IP incorrecta:**
   ```bash
   # Verifica tu IP pública
   curl -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text"
   ```

### ❌ Contenedor backend se reinicia constantemente

```bash
# Ver logs del backend
docker-compose logs backend

# Causas comunes:
# - API key inválida en .env
# - Error en el código
# - Falta alguna dependencia
```

**Solución:**
```bash
# Editar .env
nano ~/news-generator/backend/.env

# Reiniciar
docker-compose restart backend
```

### ❌ Error "Permission denied" con Docker

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y volver a conectar por SSH
exit
# Volver a conectar con ssh...
```

### ❌ Sin espacio en disco

```bash
# Limpiar imágenes y contenedores antiguos
docker system prune -a

# Ver espacio en disco
df -h
```

---

## Gestión de Costos

### Capa Gratuita (12 meses):
- ✅ **B1s VM:** 750 horas/mes gratis
- ✅ **Disco:** 64 GB gratis
- ✅ **IP pública:** Primera IP estática gratis
- ✅ **Ancho de banda:** 100 GB salida gratis/mes

### Después de 12 meses:
- **B1s VM:** ~$7.50/mes
- **Disco:** ~$0.50/mes
- **Total:** ~$8-10/mes

### Optimización:
- Apaga la VM cuando no la uses (Portal → Stop)
- Usa VM de menor tamaño si es suficiente
- Considera Azure App Service para producción

---

## Próximos Pasos Opcionales

### 1. Configurar Dominio Personalizado
- Compra un dominio (Namecheap, GoDaddy, etc.)
- Crea registro A apuntando a tu IP de Azure
- Configura DNS en Azure DNS Zones

### 2. Agregar HTTPS con Let's Encrypt
```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tudominio.com
```

### 3. Configurar Auto-deploy desde GitHub
- Usar GitHub Actions
- Deploy automático al hacer push

### 4. Monitoreo
- Azure Monitor (incluido)
- Application Insights
- Logs en Azure Log Analytics

---

## Apagar/Encender VM (Ahorrar créditos)

### Desde Azure Portal:
1. Ve a tu VM
2. Click en **"Stop"** (no se cobra mientras está detenida)
3. Para iniciar: Click en **"Start"**

### Desde CLI:
```bash
# Instalar Azure CLI en tu PC
az login
az vm stop --resource-group news-generator-rg --name news-generator-vm
az vm start --resource-group news-generator-rg --name news-generator-vm
```

---

## Eliminar Todo (Limpiar recursos)

Si quieres eliminar el proyecto completamente:

1. Azure Portal → Resource Groups
2. Selecciona `news-generator-rg`
3. Click **"Delete resource group"**
4. Escribe el nombre del grupo para confirmar
5. Click **"Delete"**

Esto elimina: VM, discos, IPs, networking, etc.

---

## ✅ Checklist de Despliegue

- [ ] VM creada con Ubuntu 22.04 LTS
- [ ] Tamaño B1s seleccionado (free tier)
- [ ] Clave SSH descargada (.pem)
- [ ] Puertos 22, 3000, 8000 abiertos en NSG
- [ ] Conectado por SSH exitosamente
- [ ] Script setup-azure.sh ejecutado
- [ ] Archivo .env configurado con API keys reales
- [ ] Contenedores corriendo (docker-compose ps)
- [ ] Frontend accesible en navegador
- [ ] Backend health endpoint responde

---

**¿Necesitas ayuda?** Revisa los logs con `docker-compose logs -f` o verifica la configuración de red en Azure Portal.
