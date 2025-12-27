# 🚀 Guía de Despliegue - FoodieAI

> Guía completa para desplegar FoodieAI en AWS EC2 con Docker.

## 📋 Contenido

- [Información del Servidor](#-información-del-servidor)
- [Requisitos](#-requisitos)
- [Conexión al Servidor](#-conexión-al-servidor)
- [Estructura de Contenedores](#-estructura-de-contenedores)
- [Deploy del Frontend](#-deploy-del-frontend)
- [Deploy del Backend](#-deploy-del-backend)
- [Verificación](#-verificación)
- [Troubleshooting](#-troubleshooting)
- [Recursos AWS](#-recursos-aws)

---

## 🖥️ Información del Servidor

| Recurso | Valor |
|---------|-------|
| **Instance ID** | `i-0ebc8f3662c3ea0cb` |
| **IP Pública** | `18.216.22.178` |
| **Región** | `us-east-2` (Ohio) |
| **Sistema Operativo** | Amazon Linux 2023 |
| **Usuario SSH** | `ec2-user` |
| **Dominio** | `foodie.softprimesolutions.com` |

---

## 📦 Requisitos

### Local (tu máquina)
- AWS CLI configurado (`aws configure`)
- SSH key (`~/.ssh/id_ed25519` o similar)
- Node.js 18+ (para build del frontend)
- Git

### Verificar AWS CLI
```bash
aws sts get-caller-identity
```

---

## 🔌 Conexión al Servidor

### Paso 1: Enviar clave pública SSH (temporal)

```powershell
aws ec2-instance-connect send-ssh-public-key `
  --instance-id i-0ebc8f3662c3ea0cb `
  --instance-os-user ec2-user `
  --ssh-public-key file://~/.ssh/id_ed25519.pub `
  --availability-zone us-east-2a
```

**Nota:** Este comando da acceso temporal (60 segundos) para iniciar la conexión.

### Paso 2: Conectar vía SSH

```bash
ssh -i ~/.ssh/id_ed25519 ec2-user@18.216.22.178
```

### Script combinado (PowerShell)

```powershell
# Enviar clave y conectar inmediatamente
aws ec2-instance-connect send-ssh-public-key `
  --instance-id i-0ebc8f3662c3ea0cb `
  --instance-os-user ec2-user `
  --ssh-public-key file://~/.ssh/id_ed25519.pub `
  --availability-zone us-east-2a; `
ssh -i ~/.ssh/id_ed25519 ec2-user@18.216.22.178
```

---

## 🐳 Estructura de Contenedores

```
┌──────────────────────────────────────────────────────┐
│                    EC2 Instance                       │
│                                                       │
│   ┌─────────────────┐    ┌─────────────────────┐     │
│   │  nginx-proxy    │    │  foodieai-backend   │     │
│   │  (Port 80/443)  │───▶│  (Port 8000)        │     │
│   └─────────────────┘    └─────────────────────┘     │
│          │                                            │
│          │ Sirve archivos estáticos                  │
│          ▼                                            │
│   /var/www/html/                                     │
│   └── (frontend build)                               │
└──────────────────────────────────────────────────────┘
```

### Ver contenedores activos

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## 🎨 Deploy del Frontend

### Paso 1: Build local

```bash
cd frontend
npm run build
```

Esto genera la carpeta `dist/` con los archivos estáticos.

### Paso 2: Copiar build al servidor

```powershell
# Enviar clave SSH
aws ec2-instance-connect send-ssh-public-key `
  --instance-id i-0ebc8f3662c3ea0cb `
  --instance-os-user ec2-user `
  --ssh-public-key file://~/.ssh/id_ed25519.pub `
  --availability-zone us-east-2a

# Copiar dist/ al servidor
scp -i ~/.ssh/id_ed25519 -r frontend/dist/* ec2-user@18.216.22.178:~/frontend-dist/
```

### Paso 3: Actualizar contenedor Nginx

```bash
# SSH al servidor
ssh -i ~/.ssh/id_ed25519 ec2-user@18.216.22.178

# En el servidor:
docker cp ~/frontend-dist/. nginx-proxy:/var/www/html/
docker exec nginx-proxy nginx -s reload
```

### Script completo (PowerShell)

```powershell
# Build + Deploy Frontend
cd frontend
npm run build

aws ec2-instance-connect send-ssh-public-key `
  --instance-id i-0ebc8f3662c3ea0cb `
  --instance-os-user ec2-user `
  --ssh-public-key file://~/.ssh/id_ed25519.pub `
  --availability-zone us-east-2a

scp -i ~/.ssh/id_ed25519 -r dist/* ec2-user@18.216.22.178:~/frontend-dist/

# Luego en el servidor ejecutar:
# docker cp ~/frontend-dist/. nginx-proxy:/var/www/html/
# docker exec nginx-proxy nginx -s reload
```

---

## ⚙️ Deploy del Backend

### Opción A: Rebuild del contenedor

```bash
# En el servidor
cd ~/restaurant-recommender-ml/backend
git pull origin main
docker build -t foodieai-backend .
docker stop foodieai-backend && docker rm foodieai-backend
docker run -d --name foodieai-backend -p 8000:8000 foodieai-backend
```

### Opción B: Actualización sin rebuild

Si solo cambiaron archivos Python:

```bash
# Copiar archivos actualizados al contenedor
docker cp src/. foodieai-backend:/app/src/
docker restart foodieai-backend
```

---

## ✅ Verificación

### Verificar URLs en producción

```bash
# Health check
curl https://foodie.softprimesolutions.com/api/v1/health/status

# API Docs
curl -I https://foodie.softprimesolutions.com/api/v1/docs

# Frontend
curl -I https://foodie.softprimesolutions.com
```

### Verificar logs

```bash
# Logs del backend
docker logs foodieai-backend --tail 50

# Logs del nginx
docker logs nginx-proxy --tail 50

# Seguir logs en tiempo real
docker logs -f foodieai-backend
```

### Verificar servicios internos

```bash
# Estado de contenedores
docker ps

# Uso de recursos
docker stats --no-stream
```

---

## 🐛 Troubleshooting

### Error: "Connection refused"

```bash
# Verificar que el contenedor está corriendo
docker ps -a | grep foodieai

# Reiniciar contenedor
docker restart foodieai-backend
```

### Error: "Permission denied" al hacer SCP

```bash
# Asegurarse de enviar la clave primero
aws ec2-instance-connect send-ssh-public-key ...

# Intentar SCP inmediatamente (60s de ventana)
scp ...
```

### Error: Frontend no se actualiza

```bash
# Limpiar cache de nginx
docker exec nginx-proxy nginx -s reload

# Verificar que los archivos se copiaron
docker exec nginx-proxy ls -la /var/www/html/
```

### Error: Backend no responde

```bash
# Ver logs de error
docker logs foodieai-backend --tail 100

# Reiniciar contenedor
docker restart foodieai-backend

# Si persiste, rebuild
docker build -t foodieai-backend . && docker restart foodieai-backend
```

### Error: Certificado SSL

Los certificados SSL son manejados por Certbot/Let's Encrypt. 
Revisar con:

```bash
docker exec nginx-proxy certbot certificates
```

---

## 📁 Recursos AWS

### S3 Bucket (assets estáticos)

| Recurso | Valor |
|---------|-------|
| **Bucket Name** | `foodieai-assets` |
| **Región** | `us-east-2` |
| **URL Base** | `https://foodieai-assets.s3.us-east-2.amazonaws.com` |

#### Archivos en S3:
- `video-tutorial.mp4` - Video tutorial del sistema
- Otros assets estáticos

### Subir archivo a S3

```bash
aws s3 cp archivo.mp4 s3://foodieai-assets/archivo.mp4 --acl public-read
```

---

## 📊 Monitoreo

### Métricas básicas

```bash
# CPU y memoria de contenedores
docker stats

# Espacio en disco
df -h

# Conexiones activas
netstat -tlnp
```

### Logs importantes

```bash
# Logs del sistema
sudo journalctl -u docker --since "1 hour ago"

# Logs de nginx
docker logs nginx-proxy --since "1h"
```

---

## 🔄 Rollback

Si algo sale mal, hacer rollback al último build funcional:

```bash
# Ver imágenes disponibles
docker images

# Revertir a imagen anterior
docker stop foodieai-backend
docker rm foodieai-backend
docker run -d --name foodieai-backend -p 8000:8000 foodieai-backend:previous_tag
```

---

## 📝 Checklist de Deploy

- [ ] Build local exitoso (`npm run build`)
- [ ] Tests pasando (`npm run test`)
- [ ] AWS CLI configurado
- [ ] Clave SSH enviada
- [ ] Archivos copiados al servidor
- [ ] Contenedor actualizado
- [ ] Nginx recargado
- [ ] URLs de producción verificadas
- [ ] Logs sin errores

---

*Última actualización: Enero 2025*
