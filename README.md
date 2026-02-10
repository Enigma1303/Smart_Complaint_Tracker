# Smart Complaint Tracker – Backend

This is a Django REST Framework backend application for managing public complaints.
The project uses PostgreSQL as the database and is fully containerized using Docker.

---

## Tech Stack

- Python 
- Django
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- JWT Authentication
- Swagger / OpenAPI (drf-spectacular)

---

## Setup (Docker)

### Prerequisites
- Docker
- Docker Compose

Clone the repository:
```bash
git clone <repository-url>
cd SMART_COMPLAINT_TRACKER
```

Create a `.env` file in the project root:
```env
DEBUG=True
DB_NAME=complaints_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Build and start the containers:
```bash
docker compose build
docker compose up
```

Run database migrations:
```bash
docker compose exec web python manage.py migrate
```

(Optional) Create admin user:
```bash
docker compose exec web python manage.py createsuperuser
```

Stop the application:
```bash
docker compose down
```

---

## Access URLs

- API Root: http://localhost:8000/
- Swagger API Documentation: http://localhost:8000/api/schema/swagger-ui/
- Django Admin Panel: http://localhost:8000/admin/

---

## Notes

- Docker installs all dependencies from requirements.txt
- Swagger (OpenAPI) is used for API documentation and testing
- Logging and exception handling are implemented in views

---

## Academic Purpose

This project demonstrates REST API development, Docker-based deployment,
logging and exception handling, and API documentation using OpenAPI.
