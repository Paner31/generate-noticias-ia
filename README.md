# News Generator

Sistema de generación de artículos de noticias usando AI. Busca fuentes con Perplexity y genera artículos profesionales con OpenRouter.

## Requisitos Previos

### Opción 1: Docker (Recomendado)
- **Docker** y **Docker Compose**
- Claves API:
  - [Perplexity API Key](https://www.perplexity.ai/)
  - [OpenRouter API Key](https://openrouter.ai/)

### Opción 2: Manual
- **Python 3.9+**
- **Node.js 18+** y **npm**
- Claves API:
  - [Perplexity API Key](https://www.perplexity.ai/)
  - [OpenRouter API Key](https://openrouter.ai/)

## Instalación y Ejecución

### Opción 1: Docker (Recomendado) 🐳

La forma más fácil y rápida de ejecutar el proyecto:

```bash
# 1. Clonar el repositorio (si aún no lo has hecho)
git clone <repo-url>
cd news-generator

# 2. Configurar variables de entorno
copy .env.example backend/.env
# Editar backend/.env y agregar tus API keys

# 3. Construir y ejecutar con Docker Compose
docker-compose up --build

# O ejecutar en segundo plano:
docker-compose up -d --build
```

**La aplicación estará disponible en:**
- Frontend: **http://localhost:3000**
- Backend API: **http://localhost:8000**
- Documentación API: **http://localhost:8000/docs**

**Comandos útiles:**
```bash
# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache
```

---

### Opción 2: Instalación Manual

#### 1. Backend (Python/FastAPI)

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
```

#### 2. Frontend (React/TypeScript)

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
copy .env.example .env
```

#### 3. Ejecución (Solo 2 Terminales)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python -m app.main
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Abre tu navegador en **http://localhost:5173**

---

## Estructura del Proyecto

```
news-generator/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints de la API
│   │   │   ├── search.py     # Búsqueda con Perplexity
│   │   │   └── generate.py   # Generación de notas
│   │   ├── core/             # Configuración
│   │   │   ├── config.py     # Variables de entorno
│   │   │   └── session_storage.py  # Almacenamiento temporal
│   │   ├── models/           # Schemas de Pydantic
│   │   │   └── schemas.py
│   │   ├── services/         # Lógica de negocio
│   │   │   ├── perplexity_service.py    # Cliente Perplexity
│   │   │   ├── openrouter_service.py    # Cliente OpenRouter
│   │   │   ├── content_fetcher.py       # Obtención de contenido
│   │   │   └── note_generator.py        # Generador de notas
│   │   └── main.py           # Punto de entrada
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── SearchForm.tsx
│   │   │   ├── SearchResults.tsx
│   │   │   ├── GeneratedNotes.tsx
│   │   │   └── ConfigPanel.tsx
│   │   ├── services/         # Cliente API
│   │   │   └── api.ts
│   │   ├── types/            # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── .dockerignore
│   ├── package.json
│   └── .env.example
├── docker-compose.yml
├── .env.example
└── README.md
```

## Arquitectura

### Backend
- **FastAPI**: Framework web asíncrono
- **Perplexity API**: Búsqueda de noticias con IA
- **OpenRouter API**: Generación de artículos con modelos LLM
- **Jina Reader**: Extracción de contenido completo de URLs
- **Procesamiento síncrono**: Las notas se generan secuencialmente y se devuelven cuando están listas

### Frontend
- **React 19**: Biblioteca UI con hooks modernos
- **TypeScript**: Type safety
- **Vite**: Build tool rápido
- **Tailwind CSS**: Styling
- **Axios**: Cliente HTTP
- **Marked**: Renderizado de Markdown

### Flujo de Trabajo
1. Usuario ingresa búsqueda → Perplexity busca fuentes
2. Usuario selecciona URLs → Frontend envía petición
3. Backend obtiene contenido completo → Jina Reader
4. Backend genera artículo → OpenRouter (Claude/GPT)
5. Backend genera contenido social → OpenRouter
6. Frontend muestra notas completas

## Configuración de Producción

### Variables de Entorno

**Backend (`backend/.env`):**
```env
PERPLEXITY_API_KEY=pplx-xxx
OPENROUTER_API_KEY=sk-or-v1-xxx
BACKEND_PORT=8000
FRONTEND_URL=https://tu-dominio.com
MAX_NOTES_PER_GENERATION=5
DEFAULT_MAX_TOKENS=8000
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

**Frontend (build arg en Docker):**
```env
VITE_API_URL=https://api.tu-dominio.com
```

### Deploy con Docker

Para producción, modifica `docker-compose.yml`:

```yaml
# Cambia los puertos
ports:
  - "443:80"  # Frontend con HTTPS
  - "8000:8000"  # Backend

# Agrega volúmenes para SSL
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

## Tecnologías

- **Backend:** FastAPI, Perplexity API, OpenRouter API, httpx
- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS, Axios
- **Deployment:** Docker, Docker Compose, Nginx

## Notas Importantes

- ⏱️ La generación de notas puede tomar 2-5 minutos dependiendo de la cantidad
- 🔑 Necesitas créditos en Perplexity y OpenRouter
- 🌐 Timeout configurado a 10 minutos para generaciones largas
- 📦 Docker usa build multi-stage para optimizar tamaño de imágenes
- 🔒 Las API keys nunca se exponen al frontend
