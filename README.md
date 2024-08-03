# SalesAdvisor

SalesAdvisor is a comprehensive solution designed to assist sales organizations in managing and analyzing their sales data effectively. The platform offers various features including user management, role-based access control, and insightful analytics to help improve sales performance.

## Features

- User Registration and Login with Google Single Sign-On
- Role-Based Access Control
- Sales Data Querying and Analytics
- Automated Product Description Generation using Celery and LLM
- API Documentation with DRF Spectacular


## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/sales-advisor.git
    cd sales-advisor
    ```

2. **Create and start Docker containers**:

    ```bash
    docker-compose up --build
    ```

### Accessing the Application

- The backend API will be available at [http://localhost:8000](http://localhost:8000)
- The frontend will be available at [http://localhost:5713](http://localhost:5713)

## API Documentation

API documentation is available via DRF Spectacular. Access the following endpoints to view the documentation:

- **Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
- **Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- **Redoc**: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

## Running Tests

To run the backend tests, use the following command inside the backend container:

```bash
docker-compose exec backend python manage.py test
docker-compose exec frontend npm test
