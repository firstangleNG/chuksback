# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

RepairHub (also known as ChukTicketingSystem) is a Django-based repair shop management system that handles customer electronics repair workflows. The system manages repair tickets, inventory, invoicing, customer data, and includes role-based user management with technicians, admins, and super admins.

## Architecture

### Core Applications Structure
- **`users/`** - Custom user authentication system with role-based access (admin, technician, superadmin)
- **`repairs/`** - Core repair ticket management, device properties, and technician assignments  
- **`customers/`** - Customer information management with search capabilities
- **`inventory/`** - Parts inventory, stock management, suppliers, and sales tracking
- **`invoice/`** - Billing system with PayPal integration and automated email invoicing
- **`dashboard/`** - Analytics and reporting dashboard
- **`logs/`** - Activity logging system

### Key Design Patterns
- **Environment-based settings**: Separate configuration files (`local.py`, `production.py`) extending `base.py`
- **Custom user model**: Email-based authentication with phone number validation using international formatting
- **UUID primary keys**: Most models use UUIDs instead of auto-incrementing integers
- **Celery async tasks**: Background email processing for notifications and invoices
- **DRF API**: REST API endpoints with JWT authentication for frontend integration

### Database Schema Highlights
- **Repair workflow**: Customer → Property → RepairTicket → Payments/Invoice chain
- **User roles**: Role-based permissions for different access levels
- **Audit trails**: Created/updated timestamps and activity logging throughout

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Database setup (requires PostgreSQL)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic --no-input
```

### Running the Application
```bash
# Development server (local environment)
DJANGO_ENV=local python manage.py runserver

# Production server with gunicorn
gunicorn repair.wsgi:application

# Run Celery worker (for background tasks)
celery -A repair worker --loglevel=info
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Database shell
python manage.py dbshell

# Django shell with models access
python manage.py shell
```

### Testing Commands
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test repairs

# Run with coverage (if installed)
coverage run --source='.' manage.py test
coverage report
```

### Deployment and Build
```bash
# Production deployment script
./build.sh

# Docker deployment
docker-compose up -d db  # Start PostgreSQL container
```

## Configuration Management

### Environment Variables Required
```env
# Core Django settings
DJANGO_ENV=local|production
SECRET_KEY=your_secret_key
DEBUG=True|False

# Database configuration
DB_NAME=repair_db
DB_USER=repair_user  
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email settings (Gmail SMTP)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# PayPal integration
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
PAYPAL_MODE=sandbox|live

# Celery (for production)
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
```

### Settings Architecture
- **`repair/settings/base.py`** - Shared configuration
- **`repair/settings/local.py`** - Development with debug mode, local database
- **`repair/settings/production.py`** - Production with security headers, external database

## API Integration

The system exposes REST API endpoints documented in `API_DOCUMENTATION.md`:
- Authentication: JWT-based with session fallback
- CORS configured for frontend integration (Next.js on Vercel)
- Main endpoints: `/api/customers/`, `/repairs/`, `/inventory/`, `/invoicing/`, `/dashboard/`

## Business Logic Key Points

### Repair Workflow States
```
New → Assigned → Diagnosed → In Progress → Awaiting Parts → Completed → Closed
```
Alternative paths: On Hold, Canceled

### User Role Hierarchy
- **Superadmin**: Full system access
- **Admin**: Management functions, user creation  
- **Technician**: Repair ticket handling, customer interaction

### Payment Integration
- Multiple payment methods supported (Cash, Card, PayPal, Bank Transfer)
- PayPal SDK integration with sandbox/live mode switching
- Automated invoice generation and email delivery

## Development Considerations

### Database Requirements
- PostgreSQL with specific extensions (ArrayField usage in repairs/models.py)
- UUID field support required
- Phone number validation using international format (+1234567890)

### Async Task Processing
- Celery handles email notifications, invoice sending, and OTP delivery
- Tasks are wrapped with `TaskWithOnCommit` for transaction safety
- Requires message broker (RabbitMQ/Redis) in production

### Frontend Integration Notes
- CORS headers configured for cross-origin requests
- JWT tokens stored in HTTP-only cookies for security
- API returns consistent JSON response format with success/error patterns

### Deployment Architecture
- Render.com deployment configuration in `render.yaml`
- Gunicorn WSGI server with Unix socket configuration
- Static file handling for production
- Separate Celery worker processes for background tasks
