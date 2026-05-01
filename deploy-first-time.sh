#!/bin/bash
# deploy-first-time.sh — Primera instalación en el droplet
# Ejecutar UNA sola vez después de clonar el repo.
# Requiere: .env ya creado con los valores de producción.

set -e

if [ ! -f .env ]; then
    echo "ERROR: No existe .env. Copia .env.example a .env y completa los valores."
    exit 1
fi

echo "==> [1/5] Construyendo imagen Django..."
docker compose build

echo "==> [2/5] Levantando base de datos..."
docker compose up -d db
echo "     Esperando que PostgreSQL inicialice..."
sleep 8

echo "==> [3/5] Levantando todos los servicios..."
docker compose up -d

echo "==> [4/5] Creando superusuario de Django..."
echo "     (Completa nombre de usuario, email y contraseña)"
docker compose exec web python manage.py createsuperuser

echo "==> [5/5] Verificando estado..."
docker compose ps

echo ""
echo "✓ Instalación completada."
echo ""
echo "Próximos pasos:"
echo "  1. Visitar http://TU_IP/admin/ y completar la ConfiguracionSitio"
echo "  2. Cuando tengas dominio y SSL, editar nginx/conf.d/app.conf"
echo "  3. Para SSL: docker run --rm certbot/certbot certonly --webroot ..."
echo "  4. Para updates futuros: ./deploy.sh"
