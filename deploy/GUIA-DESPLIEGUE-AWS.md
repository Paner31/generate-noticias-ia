# Guía de Despliegue en AWS EC2

## Paso 1: Crear Instancia EC2

1. Ve a la **Consola de AWS** → Busca "EC2"
2. Click en **"Launch Instance"** (Lanzar instancia)
3. Configura:
   - **Name:** `news-generator-server`
   - **AMI:** Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance type:** `t2.micro` (Free tier eligible)
   - **Key pair:**
     - Click "Create new key pair"
     - Name: `news-generator-key`
     - Type: RSA
     - Format: `.pem` (para SSH)
     - **¡DESCARGA Y GUARDA ESTE ARCHIVO! Lo necesitarás para conectarte**

## Paso 2: Configurar Security Group (Firewall)

En la misma pantalla de "Launch Instance":

1. En **Network settings**, click "Edit"
2. **Security group name:** `news-generator-sg`
3. Agrega las siguientes reglas:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| SSH | TCP | 22 | My IP | Conexión SSH |
| Custom TCP | TCP | 8000 | Anywhere (0.0.0.0/0) | Backend API |
| Custom TCP | TCP | 3000 | Anywhere (0.0.0.0/0) | Frontend |
| HTTP | TCP | 80 | Anywhere (0.0.0.0/0) | HTTP (opcional) |

4. Click **"Launch Instance"**
5. Espera 2-3 minutos hasta que el estado sea "Running" (verde)

## Paso 3: Obtener IP Pública

1. En EC2 Dashboard, selecciona tu instancia
2. Copia la **"Public IPv4 address"** (ejemplo: 54.123.45.67)

## Paso 4: Conectar por SSH

### En Windows (usando PowerShell o CMD):

```bash
# Navega a donde descargaste el .pem
cd Downloads

# Conecta (reemplaza con tu IP)
ssh -i news-generator-key.pem ubuntu@TU_IP_PUBLICA
```

**Ejemplo:**
```bash
ssh -i news-generator-key.pem ubuntu@54.123.45.67
```

Si tienes error de permisos en Windows, ignóralo o usa WSL/Git Bash.

## Paso 5: Ejecutar Script de Instalación

Una vez conectado por SSH:

```bash
# Descargar el script de instalación
curl -o setup-ec2.sh https://raw.githubusercontent.com/TU_USUARIO/news-generator/main/deploy/setup-ec2.sh

# Dar permisos de ejecución
chmod +x setup-ec2.sh

# Ejecutar
bash setup-ec2.sh
```

El script te pedirá:
1. La URL de tu repositorio GitHub
2. Que configures las variables de entorno (API keys)

## Paso 6: Configurar Variables de Entorno

Cuando el script te lo pida, edita el archivo `.env`:

```bash
nano ~/news-generator/backend/.env
```

Agrega tus credenciales reales:
```env
OPENAI_API_KEY=sk-tu-api-key-real
# Otras variables que necesites
```

**Guardar:** `Ctrl + O`, Enter, `Ctrl + X`

## Paso 7: Verificar Despliegue

1. Ve a tu navegador:
   - Frontend: `http://TU_IP_PUBLICA:3000`
   - Backend API: `http://TU_IP_PUBLICA:8000/health`

2. Ver logs en tiempo real:
```bash
cd ~/news-generator
docker-compose logs -f
```

3. Ver contenedores corriendo:
```bash
docker-compose ps
```

## Comandos Útiles

```bash
# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Iniciar nuevamente
docker-compose up -d

# Ver uso de recursos
docker stats

# Actualizar código desde GitHub
cd ~/news-generator
git pull
docker-compose up -d --build
```

## Solución de Problemas

### Error: "Connection refused" al acceder
- Verifica que los contenedores estén corriendo: `docker-compose ps`
- Revisa logs: `docker-compose logs`
- Verifica Security Group en AWS

### Contenedor se detiene inmediatamente
- Revisa logs específicos: `docker-compose logs backend`
- Verifica que el `.env` esté configurado correctamente

### Sin espacio en disco
- Limpiar imágenes: `docker system prune -a`

## Próximos Pasos (Opcional)

1. **Dominio personalizado:** Configurar Route 53
2. **HTTPS:** Instalar Nginx con Let's Encrypt
3. **Base de datos:** Agregar RDS o MongoDB
4. **Monitoreo:** CloudWatch o Datadog

## Costos Estimados

- **12 meses:** GRATIS (Free Tier)
- **Después:** ~$8-10/mes (t2.micro)
- **Optimización:** Puedes usar Reserved Instances para ahorrar

---

**¿Necesitas ayuda?** Revisa los logs o contacta soporte.
