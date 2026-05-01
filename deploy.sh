#!/bin/bash
# deploy.sh — Actualizar smartsolutions-web en producción
# Uso: ./deploy.sh
# Requiere: docker, docker compose, .env en el mismo directorio

set -e

echo "==> [1/4] Bajando cambios de GitHub..."
git pull origin main

echo "==> [2/4] Reconstruyendo imagen Django..."
docker compose build web

echo "==> [3/4] Reiniciando servicios (zero-downtime para nginx y db)..."
docker compose up -d --force-recreate web

echo "==> [4/4] Verificando estado..."
docker compose ps
docker compose logs --tail=20 web

echo ""
echo "✓ Deploy completado."
echo "  Admin: https://\$(grep ALLOWED_HOSTS .env | cut -d= -f2 | cut -d, -f1)/admin/"
