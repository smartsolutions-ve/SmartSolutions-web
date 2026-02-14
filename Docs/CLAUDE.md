# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SmartSolutions VE - A Django-based landing page and lead management system for a Venezuelan PYME consulting company. The application provides a public-facing landing page showcasing services, testimonials, and success cases, along with a Django admin panel for content management and lead tracking.

## Development Commands

All commands are run from the `smartsolutions/` directory:

```bash
cd smartsolutions/

# Development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic --noinput

# Django shell
python manage.py shell

# Run specific app migrations
python manage.py migrate core
python manage.py migrate landing
```

## Initial Setup

1. Copy environment file: `cp .env.example .env` and configure values
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Access admin at `http://localhost:8000/admin/` and create the initial ConfiguracionSitio record

## Architecture

### Apps Structure

- **`apps.core`**: Global site configuration and shared utilities
  - `ConfiguracionSitio` model (singleton pattern) - stores all site-wide settings
  - Context processor injects `config` variable into all templates

- **`apps.landing`**: Public-facing landing page and lead management
  - `Servicio`, `Testimonio`, `CasoDeExito` - content models
  - `Lead` - contact form submissions with state management
  - Email notifications via Resend API when leads are created

### Key Design Patterns

**Singleton ConfiguracionSitio:**
- Only one instance allowed (enforced in `save()` method with `pk=1`)
- Retrieved via `ConfiguracionSitio.get_config()` classmethod
- Automatically available in all templates as `{{ config.nombre_empresa }}`, etc.
- Edit via admin panel at `/admin/core/configuracionsitio/`

**Lead Management Flow:**
1. User submits contact form → `contacto_submit` view
2. Form validates → Lead saved to database with IP capture
3. Email notification sent to team via Resend API
4. HTMX-aware responses (returns partial HTML if HTMX request, otherwise full page redirect)

**Admin Customization:**
- Uses Django Unfold for modern UI (must be listed before `django.contrib.admin` in INSTALLED_APPS)
- Custom sidebar navigation configured in `settings.UNFOLD['SIDEBAR']`
- Color scheme customized to match SmartSolutions branding (blue #0284C7)
- Lead model has custom badges and is read-only (cannot be created from admin)

### Database

PostgreSQL database configured via environment variables:
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- Models use standard Django ORM patterns
- Models with `orden` field support manual ordering in admin

### Email System

- Uses Resend API for transactional emails
- Configured via `RESEND_API_KEY` environment variable
- Email notifications sent when new leads are created
- Gracefully handles email failures (lead is still saved to database)

### Static Files & Media

- Static files: `static/` directory, served via Whitenoise in production
- Media uploads: `media/` directory for images (testimonials, case studies)
- `STATICFILES_STORAGE` uses Whitenoise's compressed manifest storage

### Settings & Configuration

- Settings module: `config/settings.py`
- Language: Spanish (Venezuela) - `es-ve`
- Timezone: `America/Caracas`
- Security features auto-enabled when `DEBUG=False`
- CORS headers configured for potential API usage

## Important Notes

- The Django project is in the `smartsolutions/` subdirectory, not the repository root
- ConfiguracionSitio is a singleton - there should only ever be one record
- Lead models cannot be created via admin (only through public form submission)
- HTMX is expected in the frontend for dynamic form submissions
- All admin models use Django Unfold's `ModelAdmin` base class
- Spanish is used throughout (comments, verbose names, field labels)
