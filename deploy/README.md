# 🚀 Guías de Despliegue

Este directorio contiene scripts y guías para desplegar News Generator en diferentes plataformas cloud.

## 📋 Opciones Disponibles

### ☁️ Azure (Recomendado actualmente)
- **Archivo:** [GUIA-DESPLIEGUE-AZURE.md](./GUIA-DESPLIEGUE-AZURE.md)
- **Script:** [setup-azure.sh](./setup-azure.sh)
- **Beneficios:** $200 créditos + 12 meses gratis
- **Costo después:** ~$8-10/mes

### ☁️ AWS (Alternativa)
- **Archivo:** [GUIA-DESPLIEGUE-AWS.md](./GUIA-DESPLIEGUE-AWS.md) *(si aplica)*
- **Script:** [setup-ec2.sh](./setup-ec2.sh) *(si aplica)*
- **Beneficios:** 12 meses de capa gratuita
- **Costo después:** ~$8-10/mes

## 🎯 Inicio Rápido (Azure)

### 1. Requisitos Previos
- ✅ Cuenta de Azure activa
- ✅ Repositorio en GitHub
- ✅ API Keys necesarias (OpenAI, etc.)

### 2. Pasos Rápidos

1. **Subir archivos a GitHub:**
   ```bash
   git add deploy/
   git commit -m "Add deployment scripts"
   git push
   ```

2. **Crear VM en Azure:**
   - Portal: [portal.azure.com](https://portal.azure.com)
   - Virtual Machines → Create
   - Sigue [GUIA-DESPLIEGUE-AZURE.md](./GUIA-DESPLIEGUE-AZURE.md)

3. **Ejecutar script en la VM:**
   ```bash
   curl -o setup-azure.sh https://raw.githubusercontent.com/TU_USUARIO/news-generator/main/deploy/setup-azure.sh
   chmod +x setup-azure.sh
   bash setup-azure.sh
   ```

4. **Configurar .env con tus credenciales**

5. **Acceder a tu app:**
   - Frontend: `http://TU_IP:3000`
   - Backend: `http://TU_IP:8000`

## 📚 Documentación Detallada

Para instrucciones paso a paso con capturas y solución de problemas, consulta:
- **Azure:** [GUIA-DESPLIEGUE-AZURE.md](./GUIA-DESPLIEGUE-AZURE.md)

## 🛠️ Soporte

Si encuentras problemas:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica la configuración de red/firewall
3. Consulta la sección "Solución de Problemas" en la guía correspondiente

## 📝 Notas

- Los scripts instalan Docker y Docker Compose automáticamente
- Se requiere configurar variables de entorno (API keys)
- Los puertos 3000 y 8000 deben estar abiertos en el firewall
