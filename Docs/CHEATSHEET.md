# SmartSolutions — Cheatsheet de Desarrollo

Referencia rápida de comandos para desarrollo local y deploy a producción.

---

## Workflow Básico (3 pasos)

```bash
# 1. LOCAL: Hacer cambios y pushear
cd "/home/sabh/Documentos/Smart Solutions/smartsolutions"
git add .
git commit -m "descripción del cambio"
git push origin main

# 2. PRODUCCIÓN: Conectar y bajar cambios
ssh deploy@TU_IP
git -C smartsolutions pull origin main

# 3. PRODUCCIÓN: Reiniciar
docker-compose restart web
```

---

## Desarrollo Local

```bash
# Actualizar desde GitHub
git pull origin main

# Levantar servidor de desarrollo
source venv/bin/activate
python manage.py runserver
# → http://localhost:8000

# Ver cambios no guardados
git status
git diff

# Crear commit
git add archivo.py
git commit -m "descripción"
git push origin main

# Si cambiaste models.py
python manage.py makemigrations
python manage.py migrate

# Acceder al admin
# → http://localhost:8000/admin/
```

---

## Deploy a Producción

### Deploy normal (templates, views, admin)

```bash
ssh deploy@TU_IP
cd ~
git -C smartsolutions pull origin main
docker-compose restart web
docker-compose logs -f web  # Verificar que arrancó
```

### Deploy con migraciones (cambiaste models.py)

```bash
ssh deploy@TU_IP
cd ~
git -C smartsolutions pull origin main
docker-compose exec web python manage.py migrate
docker-compose restart web
```

### Deploy con nuevas dependencias (cambió requirements.txt)

```bash
ssh deploy@TU_IP
cd ~
git -C smartsolutions pull origin main
docker-compose build web
docker-compose up -d --force-recreate web
```

### Deploy con archivos estáticos nuevos

```bash
ssh deploy@TU_IP
cd ~
git -C smartsolutions pull origin main
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
docker-compose restart web
```

---

## Comandos Útiles Producción

```bash
# Ver logs en tiempo real
docker-compose logs -f web
docker-compose logs -f nginx

# Ver estado de contenedores
docker-compose ps

# Reiniciar servicios
docker-compose restart web
docker-compose restart nginx
docker-compose restart db

# Acceder a Django shell
docker-compose exec web python manage.py shell

# Acceder a PostgreSQL
docker-compose exec db psql -U smartsolutions -d smartsolutions

# Backup de base de datos
docker-compose exec -T db pg_dump -U smartsolutions smartsolutions > backup.sql

# Ver uso de recursos
docker stats
```

---

## Rollback (deshacer deploy)

```bash
ssh deploy@TU_IP
cd ~/smartsolutions

# Ver últimos commits
git log --oneline -5

# Volver al commit anterior (cambia ABC123)
git reset --hard ABC123

cd ~
docker-compose restart web
```

---

## Variables de Entorno

### Local `.env` (desarrollo)

```bash
DEBUG=True
DB_NAME=                    # Vacío = SQLite
ALLOWED_HOSTS=localhost
SITE_URL=http://localhost:8000
```

### Producción `.env` (servidor)

```bash
DEBUG=False
DB_NAME=smartsolutions      # PostgreSQL
DB_HOST=db
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
SITE_URL=https://tu-dominio.com
```

**Ubicaciones:**
- Local: `/home/sabh/Documentos/Smart Solutions/smartsolutions/.env`
- Producción: `/home/deploy/.env` (NO `/home/deploy/smartsolutions/.env`)

---

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| No veo mis cambios en producción | `git push` local, `git pull` + `restart` producción |
| Error 500 en producción | `docker-compose logs web` |
| CSS/JS no se ven | `collectstatic --noinput` + `restart nginx` |
| Cambié `.env` y no hace efecto | `docker-compose restart web` |
| Conflicto de merge | `git reset --hard origin/main` en producción |
| Error de migración | `docker-compose exec web python manage.py migrate` |

---

## Cuándo Usar Cada Comando

| Cambio | Local | Producción |
|--------|-------|------------|
| Texto en template HTML | `runserver` | `restart web` |
| Lógica en `views.py` | `runserver` | `restart web` |
| Campo nuevo en `models.py` | `makemigrations` + `migrate` | `pull` + `migrate` + `restart` |
| Archivo CSS/JS nuevo | `runserver` | `collectstatic` + `restart nginx` |
| Nueva librería Python | `pip install` + actualizar `requirements.txt` | `build web` + `restart` |
| Cambio en admin | `runserver` | `restart web` |

---

## Git Básico

```bash
# Ver estado
git status

# Ver cambios línea por línea
git diff

# Agregar archivos específicos
git add archivo1.py archivo2.html

# Agregar todo
git add .

# Commit con mensaje
git commit -m "Fix: corrección en formulario"

# Subir a GitHub
git push origin main

# Bajar de GitHub
git pull origin main

# Ver historial
git log --oneline -10

# Ver diferencias con GitHub
git fetch
git log HEAD..origin/main --oneline
```

---

## URLs Importantes

- **Local:** http://localhost:8000
- **Admin local:** http://localhost:8000/admin/
- **Producción:** https://tu-dominio.com
- **Admin producción:** https://tu-dominio.com/admin/
- **GitHub repo:** https://github.com/smartsolutions-ve/SmartSolutions-web

---

## Contactos de Emergencia

- **Droplet IP:** `159.89.47.193` (o tu IP actual)
- **SSH:** `ssh deploy@159.89.47.193`
- **DigitalOcean:** https://cloud.digitalocean.com
- **Resend (emails):** https://resend.com

---

**Documentación completa:** `Docs/WORKFLOW_DESARROLLO.md`
