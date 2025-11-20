# 📖 Resumen del Despliegue en Azure

## 🎯 ¿Qué hicimos?

Desplegamos exitosamente la aplicación **News Generator** en Azure usando Docker.

---

## 🏗️ Arquitectura Desplegada

```
┌─────────────────────────────────────────────────────┐
│            Azure Virtual Machine (B1s)              │
│                 Ubuntu 22.04 LTS                     │
│              IP: 20.190.197.238                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │         Docker Compose                      │    │
│  │                                             │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │  Frontend Container (Nginx)          │  │    │
│  │  │  Puerto: 3000                        │  │    │
│  │  │  Tecnología: React + Vite           │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  │                    ↓                         │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │  Backend Container (FastAPI)         │  │    │
│  │  │  Puerto: 8000                        │  │    │
│  │  │  Tecnología: Python + FastAPI       │  │    │
│  │  │  APIs: Perplexity + OpenRouter      │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  │                                             │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
└─────────────────────────────────────────────────────┘
                         ↓
              Internet (Usuarios)
```

---

## 📋 Proceso Completo (Paso a Paso)

### 1️⃣ Preparación Local
- ✅ Creamos archivos de despliegue (`setup-azure.sh`, guías)
- ✅ Configuramos CORS en el backend para permitir peticiones desde Azure
- ✅ Creamos fallback para clipboard (funciona en HTTP sin HTTPS)
- ✅ Subimos todo a GitHub: https://github.com/Paner31/generate-noticias-ia

### 2️⃣ Creación de VM en Azure
- ✅ Creamos VM "Markup-Blog" con Ubuntu 22.04 LTS
- ✅ Tamaño: B1s (Free Tier - 12 meses gratis)
- ✅ Configuramos SSH con clave pública
- ✅ Descargamos `news-generator-key.pem`

### 3️⃣ Configuración de Red (Firewall)
- ✅ Abrimos puerto 22 (SSH)
- ✅ Abrimos puerto 3000 (Frontend)
- ✅ Abrimos puerto 8000 (Backend)

### 4️⃣ Instalación en el Servidor
- ✅ Conectamos por SSH
- ✅ Instalamos Docker
- ✅ Instalamos Docker Compose
- ✅ Clonamos repositorio desde GitHub

### 5️⃣ Configuración de Variables
- ✅ Configuramos `backend/.env` con:
  - API Keys (Perplexity + OpenRouter)
  - URL del frontend con IP pública
  - Configuración de puertos y límites

### 6️⃣ Ajustes de Despliegue
- ✅ Modificamos `docker-compose.yml`:
  - VITE_API_URL apuntando a IP pública (20.190.197.238:8000)
- ✅ Corregimos CORS en backend (permitir todas las peticiones)

### 7️⃣ Construcción y Despliegue
- ✅ Ejecutamos `docker-compose up -d --build`
- ✅ Frontend construido con Vite
- ✅ Backend iniciado con FastAPI + Uvicorn
- ✅ Healthcheck configurado y funcionando

### 8️⃣ Solución de Problemas
- ✅ Resolvimos error 404 en `/api/generate/` (espacios en .env)
- ✅ Resolvimos error CORS (preflight OPTIONS 400)
- ✅ Resolvimos error clipboard en HTTP (fallback sin HTTPS)
- ✅ Actualizamos API key de OpenRouter

### 9️⃣ Verificación Final
- ✅ Frontend accesible: http://20.190.197.238:3000
- ✅ Backend respondiendo: http://20.190.197.238:8000/health
- ✅ Búsqueda funcionando correctamente
- ✅ Generación de notas funcionando
- ✅ Botones de copiar funcionando (con fallback)

---

## 🔧 Tecnologías Utilizadas

### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Web Server:** Nginx Alpine
- **Styling:** Tailwind CSS
- **Markdown:** marked.js

### Backend
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn
- **APIs Externas:**
  - Perplexity AI (búsqueda)
  - OpenRouter (generación de texto)
- **Modelo:** z-ai/glm-4.6

### Infraestructura
- **Cloud:** Microsoft Azure
- **Compute:** Virtual Machine B1s
- **OS:** Ubuntu Server 22.04 LTS
- **Containerización:** Docker + Docker Compose
- **Control de Versiones:** Git + GitHub

---

## 🔑 Archivos Importantes

### Configuración
```
backend/.env              → Variables de entorno (API keys, config)
docker-compose.yml        → Orquestación de contenedores
frontend/Dockerfile       → Construcción del frontend
backend/Dockerfile        → Construcción del backend
```

### Scripts de Despliegue
```
deploy/setup-azure.sh           → Script de instalación automática
deploy/GUIA-DESPLIEGUE-AZURE.md → Guía completa paso a paso
deploy/COMANDOS-AZURE.md        → Comandos útiles (este archivo)
deploy/conectar-ssh.cmd         → Script Windows para SSH
```

---

## 🌐 URLs de Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://20.190.197.238:3000 | Interfaz de usuario |
| Backend API | http://20.190.197.238:8000 | API REST |
| Health Check | http://20.190.197.238:8000/health | Estado del servidor |
| API Docs | http://20.190.197.238:8000/docs | Swagger UI |
| ReDoc | http://20.190.197.238:8000/redoc | Documentación alternativa |

---

## 🔐 Credenciales y Acceso

### SSH
```bash
Usuario: azureuser
IP: 20.190.197.238
Clave: news-generator-key.pem (en Downloads)
Comando: ssh -i news-generator-key.pem azureuser@20.190.197.238
```

### Variables de Entorno (.env)
```env
PERPLEXITY_API_KEY=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
OPENROUTER_API_KEY=sk-or-v1-[tu-clave-actual]
BACKEND_PORT=8000
FRONTEND_URL=http://20.190.197.238:3000
MAX_NOTES_PER_GENERATION=5
DEFAULT_MAX_TOKENS=8000
OPENROUTER_MODEL=z-ai/glm-4.6
```

---

## 📊 Estado Actual del Deployment

### ✅ Funcionando Correctamente
- [x] Conexión SSH
- [x] Docker y Docker Compose instalados
- [x] Contenedores corriendo (backend + frontend)
- [x] Frontend accesible desde navegador
- [x] Backend respondiendo a peticiones
- [x] Búsqueda de noticias funcionando
- [x] Generación de notas funcionando
- [x] Botones de copiar funcionando (con fallback)
- [x] CORS configurado correctamente
- [x] Healthcheck activo

### 🔧 Configuraciones Aplicadas
- [x] CORS permitiendo todas las peticiones (`allow_origins=["*"]`)
- [x] Frontend apuntando a IP pública del backend
- [x] Clipboard con fallback para HTTP
- [x] Variables de entorno sin espacios
- [x] API keys actualizadas

---

## 💡 Problemas Resueltos Durante el Despliegue

### 1. Error 404 en `/api/generate/`
**Causa:** Espacios al inicio de líneas en `backend/.env`
**Solución:** Eliminamos espacios y reiniciamos backend

### 2. Error CORS (Preflight OPTIONS 400)
**Causa:** Backend no permitía peticiones desde IP pública
**Solución:**
- Configuramos `FRONTEND_URL` con IP pública en .env
- Cambiamos `allow_origins=["*"]` en backend/app/main.py

### 3. Botones Copy no funcionaban
**Causa:** `navigator.clipboard` no funciona en HTTP (solo HTTPS/localhost)
**Solución:** Implementamos fallback con `document.execCommand('copy')`

### 4. Frontend conectando a localhost en lugar de IP pública
**Causa:** `VITE_API_URL` en docker-compose.yml apuntaba a localhost
**Solución:** Cambiamos a `VITE_API_URL=http://20.190.197.238:8000`

---

## 📈 Métricas de Uso

### Recursos del Servidor (B1s)
- **CPU:** 1 vCPU
- **RAM:** 1 GB
- **Disco:** 30 GB SSD
- **Red:** Básica

### Contenedores
```bash
# Para ver uso en tiempo real:
docker stats

# Uso típico:
Backend:  ~200MB RAM, CPU bajo
Frontend: ~50MB RAM, CPU mínimo
```

---

## 💰 Costos

### Actual (Free Tier - 12 meses)
- **VM B1s:** GRATIS (750 horas/mes)
- **Disco:** GRATIS (64 GB incluidos)
- **IP Pública:** GRATIS (primera IP estática)
- **Ancho de banda:** GRATIS (100 GB salida/mes)

**Total:** $0/mes (primeros 12 meses)

### Después de Free Tier
- **VM B1s:** ~$7.50/mes
- **Disco:** ~$0.50/mes
- **Total estimado:** ~$8-10/mes

---

## 🚀 Próximos Pasos Sugeridos

### Seguridad
- [ ] Configurar HTTPS con Let's Encrypt
- [ ] Configurar dominio personalizado
- [ ] Restringir CORS a dominios específicos
- [ ] Rotar API keys periódicamente

### Mejoras
- [ ] Configurar CI/CD con GitHub Actions
- [ ] Agregar base de datos (PostgreSQL/MongoDB)
- [ ] Implementar caché (Redis)
- [ ] Configurar logging centralizado
- [ ] Agregar monitoreo (Azure Monitor / Datadog)

### Escalabilidad
- [ ] Migrar a Azure Container Instances
- [ ] Configurar Load Balancer
- [ ] Auto-scaling basado en demanda

---

## 📚 Recursos Útiles

### Documentación
- Azure Portal: https://portal.azure.com
- GitHub Repo: https://github.com/Paner31/generate-noticias-ia
- FastAPI Docs: https://fastapi.tiangolo.com
- Docker Docs: https://docs.docker.com

### Archivos de Referencia
- `deploy/COMANDOS-AZURE.md` → Todos los comandos útiles
- `deploy/GUIA-DESPLIEGUE-AZURE.md` → Guía completa de despliegue
- `deploy/conectar-ssh.cmd` → Script para conectar desde Windows

---

## 🆘 Contacto y Soporte

**Repositorio GitHub:** https://github.com/Paner31/generate-noticias-ia
**Issues:** https://github.com/Paner31/generate-noticias-ia/issues

---

## ✅ Checklist de Verificación

```bash
# ¿Todo funciona?
✅ SSH: ssh -i news-generator-key.pem azureuser@20.190.197.238
✅ Frontend: http://20.190.197.238:3000
✅ Backend: http://20.190.197.238:8000/health
✅ Búsqueda: Probar búsqueda en frontend
✅ Generación: Probar generar nota
✅ Copy: Probar botones de copiar
✅ Logs: sudo docker-compose logs --tail=50
```

---

**Deployment completado exitosamente el:** 19 de Noviembre, 2025
**Última actualización:** 19 de Noviembre, 2025
**Versión del deployment:** v1.0.0
