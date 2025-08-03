# Subscription Management System

A Django-based subscription management system with real-time currency exchange tracking and automated background tasks.

## Features

- **User Authentication** - JWT-based authentication system
- **Subscription Management** - Create, view, and cancel subscriptions
- **Currency Exchange** - Real-time USD to BDT exchange rate tracking
- **Background Tasks** - Automated hourly exchange rate updates
- **REST API** - Complete API endpoints with authentication
- **Admin Interface** - Django admin for data management

## Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: SQLite (Dev), MySQL (Prod)
- **Task Queue**: Celery + Redis
- **External API**: ExchangeRate-API
- **Containerization**: Docker & Docker Compose

## Quick Start

### Using Optimized multistate Docker

```bash
# Clone repository
git clone https://github.com/Md-Merazul-Islam/SUBXCHANGE.git
cd SUBXCHANGE

# Setup environment
cp .env.example .env
# Edit .env with your configurations

# Build and run
docker-compose up --build

# Run migrations and create superuser
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Local Development

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Start Redis server
redis-server

# Run development server
python manage.py runserver

# Start Celery (in separate terminals)
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info
```

## API Documentation

**📋 Postman Collection**: [Complete API Documentation](https://documenter.getpostman.com/view/40097709/2sB3BAMsMt)  
**🌐 Frontend UI**: [http://172.252.13.75:3252](http://172.252.13.75:3252/subscriptions/)  
**⚡API Base URL**: `http://172.252.13.75:3252`

### Key Endpoints

- `POST /auths/login/` - Authentication
- `POST /api/subscribe/` - Create subscription
- `GET /api/v1/exchange/exchange-rate/` - Get exchange rate

### API Examples

**1. Authentication**

```bash
POST /api-token-auth/
{
    "username": "admin",
    "password": "password"
}
```

Response:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Login successful",
  "data": {
    "access_token": "eyJ....",
    "refresh_token": "eyJ...."
  }
}
```

**2. Create Subscription**

```bash
POST /api/v1/subscription/subscribe/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
{
    "plan_id": 1
}
```

Response:

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Subscription created successfully",
  "data": {
    "id": 1,
    "user": {
      "id": 1,
      "username": "meraz",
      "email": "admin@gmail.com",
      "first_name": "",
      "last_name": ""
    },
    "plan": {
      "id": 1,
      "name": "Basic",
      "price": "9.99",
      "duration_days": 30,
      "created_at": "2025-08-01T15:36:31.390352Z",
      "updated_at": "2025-08-01T15:36:31.390352Z"
    },
    "start_date": "2025-08-01T15:52:09.710570Z",
    "end_date": "2025-08-31T15:52:09.710570Z",
    "status": "active",
    "created_at": "2025-08-01T15:52:09.711570Z",
    "updated_at": "2025-08-01T15:52:09.711570Z"
  }
}
```

**3. Get Exchange Rate**

```bash
GET /api/v1/exchange/exchange-rate/?base=USD&target=BDT
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

Response:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Exchange rate fetched",
  "data": {
    "base_currency": "USD",
    "target_currency": "BDT",
    "rate": 122.3321,
    "fetched_at": "2025-08-01T17:05:51.828607Z",
    "source": "api"
  }
}
```

## Environment Variables

Create `.env` file in project root:

```env
# Environment Setting (CHANGE THIS TO SWITCH ENVIRONMENTS)
DJANGO_ENVIRONMENT=development  # production or development

# Host Port
HOST_PORT=8000

# Core Django Settings
SECRET_KEY=

# Database Configuration (PostgreSQL)
POSTGRES_DB=your_project_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432

# Exchange Rate API
EXCHANGE_API_URL=
EXCHANGE_API_KEY=
```

## Background Tasks

Automated tasks running via Celery:

- **Exchange Rate Updates**: Fetches USD to BDT rates every hour
- **Data Logging**: Stores exchange rate history
- **Error Handling**: Graceful API failure management

## Admin Access

- **Django Admin**: ``
- **Frontend**: ``

## Testing

```bash
# Local
python manage.py test

# Docker
docker-compose exec web python manage.py test
```

## Production Deployment

1. Set `DEBUG=False` in production
2. Use PostgreSQL/MySQL for database
3. Configure proper CORS settings
4. Set up monitoring and logging
5. Use environment variables for secrets
