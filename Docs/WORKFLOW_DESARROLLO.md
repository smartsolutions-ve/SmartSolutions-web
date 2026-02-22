# Workflow de Desarrollo — SmartSolutions VE

Guía completa para trabajar en tu entorno local y actualizar el servidor de producción sin romper nada.

---

## Tabla de Contenidos

1. [Conceptos Clave](#conceptos-clave)
2. [Diferencias entre Local y Producción](#diferencias-entre-local-y-producción)
3. [Configuración de Entornos](#configuración-de-entornos)
4. [Workflow Diario](#workflow-diario)
5. [Tipos de Cambios Comunes](#tipos-de-cambios-comunes)
6. [Deploy a Producción](#deploy-a-producción)
7. [Rollback (Deshacer Deploy)](#rollback-deshacer-deploy)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Conceptos Clave

### Los 3 Entornos

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   LOCAL (DEV)   │ ───> │   GITHUB        │ ───> │  PRODUCCIÓN     │
│                 │      │                 │      │                 │
│ Tu computadora  │ push │ Repositorio     │ pull │ DigitalOcean    │
│ DEBUG=True      │      │ Código fuente   │      │ DEBUG=False     │
│ SQLite          │      │ (sin .env)      │      │ PostgreSQL      │
│ 127.0.0.1:8000  │      │                 │      │ tu-dominio.com  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

**Local (Desarrollo):**
- Trabajas aquí todos los días
- Haces cambios, pruebas, rompes cosas sin miedo
- Base de datos SQLite (se puede borrar y recrear)
- `DEBUG=True` → ves errores detallados

**GitHub:**
- Almacena el código fuente
- Es la "fuente de verdad" — lo que está en GitHub es lo oficial
- NO almacena datos sensibles (`.env` está en `.gitignore`)

**Producción:**
- El servidor en DigitalOcean donde los clientes ven el sitio
- `DEBUG=False` → no muestra errores técnicos
- Base de datos PostgreSQL real con datos de clientes (leads, testimonios)
- NUNCA hagas cambios directamente aquí — siempre desde local → GitHub → producción

---

## Diferencias entre Local y Producción

| Aspecto | Local (Dev) | Producción |
|---------|-------------|------------|
| **Ubicación** | `/home/sabh/Documentos/Smart Solutions/smartsolutions/` | `/home/deploy/smartsolutions/` |
| **Variables `.env`** | `DEBUG=True`, `ALLOWED_HOSTS=localhost` | `DEBUG=False`, `ALLOWED_HOSTS=tu-dominio.com` |
| **Base de datos** | SQLite (`db.sqlite3`) | PostgreSQL en Docker |
| **Servidor web** | `python manage.py runserver` (8000) | Gunicorn + Nginx (puerto 80/443) |
| **Archivos estáticos** | Servidos por Django directamente | Servidos por Nginx (más rápido) |
| **SSL/HTTPS** | No | Sí (Let's Encrypt) |
| **Contenedor Docker** | No (corres Python directo) | Sí (todo en contenedores) |
| **Git branch** | `main` (o puedes usar `dev`) | Siempre `main` |
| **Logs de errores** | En pantalla (terminal) | En archivos `/var/log/` |
| **Cambios en código** | Se ven automáticamente (runserver recarga) | Requiere rebuild y restart de Docker |

---

## Configuración de Entornos

### Local — archivo `.env`

```bash
# /home/sabh/Documentos/Smart Solutions/smartsolutions/.env
DEBUG=True
SECRET_KEY=cualquier-cosa-local-no-importa
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos — si DB_NAME está vacío, usa SQLite automáticamente
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email (Resend) — puedes usar el mismo API key que producción
RESEND_API_KEY=re_tu_api_key_de_resend
DEFAULT_FROM_EMAIL=noreply@smartsolutions.com.ve
CONTACT_EMAIL=tu@email.com

SITE_URL=http://localhost:8000
```

**Importante:** `DB_NAME` vacío → `settings.py` usa SQLite automáticamente.

---

### Producción — archivo `.env`

```bash
# /home/deploy/.env (en el servidor DigitalOcean)
DEBUG=False
SECRET_KEY=clave_segura_de_50_caracteres_generada_con_secrets
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# PostgreSQL (el host "db" es el contenedor de Docker)
DB_NAME=smartsolutions
DB_USER=smartsolutions
DB_PASSWORD=contraseña_segura_postgres
DB_HOST=db
DB_PORT=5432

# Email
RESEND_API_KEY=re_tu_api_key_de_resend
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com
CONTACT_EMAIL=contacto@tu-dominio.com

SITE_URL=https://tu-dominio.com
```

**Crítico:** NUNCA subas este archivo a Git. Está en `.gitignore`.

---

## Workflow Diario

### 1. Antes de empezar a trabajar: actualizar local

```bash
cd "/home/sabh/Documentos/Smart Solutions/smartsolutions"

# Bajar cambios del repositorio (por si trabajaste desde otro lado)
git pull origin main

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (por si agregaste algo nuevo)
pip install -r requirements.txt

# Migrar base de datos (por si hay cambios en modelos)
python manage.py migrate

# Levantar servidor de desarrollo
python manage.py runserver
# Abre http://localhost:8000
```

---

### 2. Hacer cambios en el código

Edita archivos normalmente:
- `apps/landing/views.py` → lógica de negocio
- `apps/landing/models.py` → modelos de base de datos
- `templates/` → HTML
- `static/` → CSS, JavaScript, imágenes

**El servidor de desarrollo (`runserver`) recarga automáticamente cuando guardas cambios.**

---

### 3. Probar los cambios localmente

```bash
# El servidor está corriendo en http://localhost:8000
# Abre el navegador y prueba:
# - Formulario de contacto funciona
# - Admin sigue funcionando (http://localhost:8000/admin/)
# - CSS se ve bien
# - No hay errores en la terminal
```

---

### 4. Si cambiaste modelos (agregaste campos a la DB)

```bash
python manage.py makemigrations
# Django genera archivo en apps/landing/migrations/0002_auto_...

python manage.py migrate
# Aplica cambios a db.sqlite3 local

# Verifica que funciona
python manage.py runserver
```

**Importante:** El archivo de migración generado (`migrations/0002_...`) SÍ se sube a Git.

---

### 5. Commit de los cambios

```bash
# Ver qué archivos cambiaron
git status

# Agregar archivos al commit
git add apps/landing/views.py
git add templates/landing/index.html
# O agregar todo:
git add .

# Ver exactamente qué cambiará antes de commitear
git diff --staged

# Crear el commit
git commit -m "Descripción clara del cambio

- Detalle 1
- Detalle 2

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Subir a GitHub
git push origin main
```

---

### 6. Deploy a producción

```bash
# Conectarte al servidor
ssh deploy@TU_IP

# Ir al directorio del proyecto
cd ~

# Bajar cambios de GitHub
git -C smartsolutions pull origin main

# Si hay nuevas migraciones, aplicarlas
docker-compose exec web python manage.py migrate

# Si agregaste dependencias en requirements.txt, rebuild
docker-compose build web

# Reiniciar Django
docker-compose up -d --force-recreate web

# Ver logs para confirmar que arrancó sin errores
docker-compose logs -f web
# Si ves "Booting worker" → todo bien
# Ctrl+C para salir
```

---

### 7. Verificar en producción

Abre `https://tu-dominio.com` en el navegador:
- ¿Se ven los cambios?
- ¿El CSS carga correctamente?
- ¿No hay errores 500?

Si todo está bien, listo. Si algo falla, ve a [Rollback](#rollback-deshacer-deploy).

---

## Tipos de Cambios Comunes

### A. Cambios solo en templates (HTML, CSS inline)

**Ejemplo:** Cambiar el texto del Hero, agregar una sección nueva en el HTML.

```bash
# Local
nano templates/landing/index.html
# Guardar cambios, probar en http://localhost:8000

git add templates/landing/index.html
git commit -m "Update: cambiar texto del Hero"
git push origin main

# Producción
ssh deploy@TU_IP
git -C smartsolutions pull origin main
docker-compose restart web
```

**No necesitas rebuild.** Solo restart.

---

### B. Cambios en views.py (lógica Python)

**Ejemplo:** Cambiar la validación del formulario de contacto.

```bash
# Local
nano apps/landing/views.py
# Guardar, probar

git add apps/landing/views.py
git commit -m "Fix: validación de email en contacto"
git push origin main

# Producción
ssh deploy@TU_IP
git -C smartsolutions pull origin main
docker-compose restart web
```

**No necesitas rebuild** (a menos que cambies dependencias).

---

### C. Cambios en models.py (base de datos)

**Ejemplo:** Agregar campo `linkedin_url` al modelo `Testimonio`.

```bash
# Local
nano apps/landing/models.py
# Agregar: linkedin_url = models.URLField(blank=True)

python manage.py makemigrations
# Genera: apps/landing/migrations/0003_testimonio_linkedin_url.py

python manage.py migrate
# Aplica a db.sqlite3 local

# Probar que funciona
python manage.py runserver

git add apps/landing/models.py
git add apps/landing/migrations/0003_testimonio_linkedin_url.py
git commit -m "Add: campo linkedin_url a Testimonio"
git push origin main

# Producción
ssh deploy@TU_IP
git -C smartsolutions pull origin main
docker-compose exec web python manage.py migrate
docker-compose restart web
```

**Importante:** SIEMPRE aplicar migraciones en producción después de hacer pull.

---

### D. Agregar una dependencia Python nueva

**Ejemplo:** Instalar `django-ratelimit` para rate limiting.

```bash
# Local
source venv/bin/activate
pip install django-ratelimit==4.1.0

# Actualizar requirements.txt
pip freeze | grep django-ratelimit >> requirements.txt
# O editarlo manualmente

# Probar que funciona
python manage.py runserver

git add requirements.txt
git commit -m "Add: django-ratelimit para rate limiting"
git push origin main

# Producción
ssh deploy@TU_IP
git -C smartsolutions pull origin main
docker-compose build web              # ← REBUILD necesario
docker-compose up -d --force-recreate web
```

**Rebuild obligatorio** porque cambió `requirements.txt`.

---

### E. Cambios en archivos estáticos (CSS, JS, imágenes)

**Ejemplo:** Agregar una nueva imagen al directorio `static/images/`.

```bash
# Local
cp nueva-imagen.png static/images/
# Usarla en el template: {% static 'images/nueva-imagen.png' %}

git add static/images/nueva-imagen.png
git commit -m "Add: imagen nueva para sección X"
git push origin main

# Producción
ssh deploy@TU_IP
git -C smartsolutions pull origin main
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

**Collectstatic obligatorio** para archivos nuevos en `static/`.

---

## Deploy a Producción

### Checklist pre-deploy

Antes de hacer deploy, verifica en local:

```bash
# 1. Todas las migraciones están aplicadas
python manage.py migrate --check

# 2. Tests pasan (si tienes tests)
python manage.py test

# 3. Collectstatic no da errores
python manage.py collectstatic --noinput --dry-run

# 4. No hay imports rotos
python manage.py check

# 5. Git status limpio (todo commiteado)
git status
```

---

### Deploy paso a paso

```bash
# 1. SSH al servidor
ssh deploy@TU_IP

# 2. Ir al directorio home
cd ~

# 3. Ver qué va a cambiar (opcional)
git -C smartsolutions fetch origin main
git -C smartsolutions log HEAD..origin/main --oneline
# Esto muestra los commits que vas a bajar

# 4. Hacer pull
git -C smartsolutions pull origin main

# 5. Aplicar migraciones (si hay)
docker-compose exec web python manage.py migrate

# 6. Collectstatic (si cambiaste archivos en static/)
docker-compose exec web python manage.py collectstatic --noinput

# 7. Rebuild (solo si cambiaste requirements.txt o Dockerfile)
docker-compose build web

# 8. Reiniciar Django
docker-compose up -d --force-recreate web

# 9. Verificar logs
docker-compose logs -f web
# Presiona Ctrl+C cuando veas "Booting worker"
```

---

### Deploy rápido (sin migraciones ni rebuild)

Si solo cambiaste templates o views:

```bash
ssh deploy@TU_IP
cd ~ && git -C smartsolutions pull origin main && docker-compose restart web
```

Una sola línea, tarda ~10 segundos.

---

## Rollback (Deshacer Deploy)

Si deployeaste algo que rompió el sitio en producción:

### Opción 1: Rollback con Git

```bash
# En el servidor
ssh deploy@TU_IP
cd ~/smartsolutions

# Ver últimos commits
git log --oneline -5

# Volver al commit anterior (cambia HASH por el commit bueno)
git reset --hard HASH_DEL_COMMIT_ANTERIOR

# Reiniciar
cd ~
docker-compose restart web
```

---

### Opción 2: Revertir el commit en local y re-deploy

```bash
# En tu computadora local
git log --oneline -5

# Revertir el commit malo (cambia HASH)
git revert HASH_DEL_COMMIT_MALO
# Esto crea un nuevo commit que deshace el anterior

git push origin main

# En producción
ssh deploy@TU_IP
git -C smartsolutions pull origin main
docker-compose restart web
```

**Opción 2 es mejor** porque mantiene el historial de Git limpio.

---

## Best Practices

### 1. NUNCA edites código directamente en producción

```bash
# ❌ MAL — nunca hagas esto en el servidor
ssh deploy@TU_IP
nano ~/smartsolutions/apps/landing/views.py

# ✅ BIEN — edita en local, commit, push, deploy
# (en tu computadora)
nano apps/landing/views.py
git commit && git push
# (en el servidor)
ssh deploy@TU_IP && git -C smartsolutions pull && docker-compose restart web
```

**Por qué:** Si editas en producción, perderás esos cambios en el próximo deploy.

---

### 2. Commits pequeños y frecuentes

```bash
# ❌ MAL
git add .
git commit -m "cambios varios"

# ✅ BIEN
git add apps/landing/views.py
git commit -m "Fix: validación de email en formulario contacto"

git add templates/landing/_hero.html
git commit -m "Update: cambiar texto del CTA principal"
```

**Por qué:** Si algo rompe, es más fácil identificar qué commit causó el problema.

---

### 3. Probar SIEMPRE en local antes de deploy

```bash
# Workflow correcto:
1. Hacer cambio en local
2. Probar en http://localhost:8000
3. Verificar que funciona
4. Commit + push
5. Deploy a producción
6. Verificar que funciona en https://tu-dominio.com
```

---

### 4. Mantener el `.env` sincronizado (pero diferente)

Ambos archivos `.env` (local y producción) deben tener **las mismas variables**, pero con **valores diferentes**:

```bash
# Local .env
DEBUG=True
DB_NAME=                    # Vacío = SQLite
ALLOWED_HOSTS=localhost

# Producción .env
DEBUG=False
DB_NAME=smartsolutions      # PostgreSQL
ALLOWED_HOSTS=tu-dominio.com
```

Si agregas una nueva variable (ej: `GOOGLE_ANALYTICS_ID`), actualiza ambos `.env`.

---

### 5. Backups antes de cambios grandes

Si vas a cambiar esquema de base de datos o hacer refactoring grande:

```bash
# En producción, hacer backup ANTES de deploy
ssh deploy@TU_IP
cd ~
docker-compose exec -T db pg_dump -U smartsolutions smartsolutions > backup_pre_deploy_$(date +%Y%m%d).sql
gzip backup_pre_deploy_*.sql
```

Si algo sale mal, puedes restaurar.

---

### 6. Usa branches para features grandes

Si vas a trabajar en algo que tardará varios días:

```bash
# Crear branch nueva
git checkout -b feature/nuevo-servicio-calculadora

# Trabajar en la feature sin tocar main
# Hacer commits normalmente
git add .
git commit -m "WIP: agregando calculadora"

# Cuando esté lista, mergear a main
git checkout main
git merge feature/nuevo-servicio-calculadora
git push origin main

# Deploy como siempre
```

**Ventaja:** `main` siempre tiene código estable listo para deploy.

---

## Troubleshooting

### "No veo mis cambios en producción"

**Posibles causas:**

1. **Olvidaste hacer push**
   ```bash
   # En local
   git status
   # Si dice "Your branch is ahead of origin/main" → falta push
   git push origin main
   ```

2. **Olvidaste hacer pull en producción**
   ```bash
   ssh deploy@TU_IP
   git -C smartsolutions status
   # Si dice "behind" → falta pull
   git -C smartsolutions pull origin main
   docker-compose restart web
   ```

3. **Cacheo de navegador**
   - Presiona `Ctrl+Shift+R` (Chrome/Firefox) para recargar sin caché
   - O abre en modo incógnito

4. **Archivos estáticos no recopilados**
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   docker-compose restart nginx
   ```

---

### "Cambié el .env en producción pero no hace efecto"

Después de cambiar `.env` en producción, **debes reiniciar**:

```bash
docker-compose restart web
```

---

### "Error 500 en producción, pero funciona en local"

1. Ver logs de producción:
   ```bash
   docker-compose logs web | tail -100
   ```

2. Causas comunes:
   - `ALLOWED_HOSTS` no incluye tu dominio
   - Falta variable en `.env` de producción
   - Falta migración: `docker-compose exec web python manage.py migrate`
   - Falta `collectstatic`

---

### "Conflicto de merge al hacer pull"

Si cambiaste el mismo archivo en local y en producción (por error):

```bash
# En producción
git -C smartsolutions status
# Dice "both modified: apps/landing/views.py"

# Ver diferencias
git -C smartsolutions diff apps/landing/views.py

# Opción 1: descartar cambios del servidor, usar lo de GitHub
git -C smartsolutions checkout apps/landing/views.py
git -C smartsolutions pull origin main

# Opción 2: guardar cambios del servidor en un archivo temporal
git -C smartsolutions diff apps/landing/views.py > ~/cambios_locales.patch
git -C smartsolutions reset --hard HEAD
git -C smartsolutions pull origin main
```

**Prevención:** NUNCA edites código en producción.

---

### "Olvidé hacer migration antes de deploy"

Si deployeaste código que usa campos nuevos pero no aplicaste la migración:

```bash
# Producción dará error 500

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Reiniciar
docker-compose restart web
```

---

## Resumen del Workflow Ideal

```
┌─────────────────────────────────────────────────────────┐
│                    TU COMPUTADORA (LOCAL)                │
├─────────────────────────────────────────────────────────┤
│ 1. git pull origin main                                 │
│ 2. Editar código (views, templates, models)             │
│ 3. python manage.py runserver → probar en localhost     │
│ 4. git add . && git commit -m "descripción"             │
│ 5. git push origin main                                 │
└─────────────────────────────────────────────────────────┘
                            ↓
                    GITHUB (Repositorio)
                            ↓
┌─────────────────────────────────────────────────────────┐
│              SERVIDOR DIGITALOCEAN (PRODUCCIÓN)          │
├─────────────────────────────────────────────────────────┤
│ 1. ssh deploy@TU_IP                                     │
│ 2. git -C smartsolutions pull origin main               │
│ 3. docker-compose exec web python manage.py migrate     │
│ 4. docker-compose restart web (o build si cambió req)   │
│ 5. docker-compose logs -f web → verificar               │
│ 6. Abrir https://tu-dominio.com → probar                │
└─────────────────────────────────────────────────────────┘
```

**Tiempo total:** ~2-5 minutos por deploy.

---

## Comandos de Referencia Rápida

```bash
# ═══════════════════════════════════════════════════════
#  LOCAL (desarrollo)
# ═══════════════════════════════════════════════════════

# Actualizar desde GitHub
git pull origin main

# Ver cambios no commiteados
git status
git diff

# Crear commit
git add .
git commit -m "descripción"
git push origin main

# Levantar servidor de desarrollo
python manage.py runserver

# Crear migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superuser
python manage.py createsuperuser


# ═══════════════════════════════════════════════════════
#  PRODUCCIÓN (servidor DigitalOcean)
# ═══════════════════════════════════════════════════════

# Conectar al servidor
ssh deploy@TU_IP

# Actualizar código
cd ~ && git -C smartsolutions pull origin main

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Recopilar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Rebuild (si cambió requirements.txt)
docker-compose build web

# Reiniciar Django
docker-compose restart web

# Ver logs
docker-compose logs -f web

# Rollback a commit anterior
git -C smartsolutions reset --hard HASH_ANTERIOR
docker-compose restart web

# Backup de base de datos
docker-compose exec -T db pg_dump -U smartsolutions smartsolutions > backup.sql
```

---

**Documentación relacionada:**
- [Guía de Deploy en DigitalOcean](./guia_deploy_digitalocean.md)
- [Documentación técnica completa](../DOCUMENTATION.md)
- [Recomendaciones de mejora](../RECOMMENDATIONS.md)
