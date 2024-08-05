https://www.loom.com/share/73f6b76d4ffe41a284eae9a23db224f6
# SalesAdvisor

SalesAdvisor is a comprehensive solution designed to assist sales organizations in managing and analyzing their sales data effectively. The platform offers various features including user management, role-based access control, and insightful analytics to help improve sales performance.

Currently i'm using csv as mock database, but we can also maintain a database of several org's databases which can be queried upon.

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

- The backend API will be available at [https://utkarsh-fse-mha4s7stfa-uc.a.run.app](https://utkarsh-fse-mha4s7stfa-uc.a.run.app)
- The frontend will be available at [http://localhost:5713](http://localhost:5713)

## API Documentation

API documentation is available via DRF Spectacular. Access the following endpoints to view the documentation:

- **Schema**: [https://utkarsh-fse-mha4s7stfa-uc.a.run.app/api/schema/](https://utkarsh-fse-mha4s7stfa-uc.a.run.app/api/schema/)
- **Swagger UI**: [https://utkarsh-fse-mha4s7stfa-uc.a.run.app/api/schema/swagger-ui/](https://utkarsh-fse-mha4s7stfa-uc.a.run.app/api/schema/swagger-ui/)
- **Redoc**: [https://utkarsh-fse-mha4s7stfa-uc.a.run.app/api/schema/redoc/](https://utkarsh-fse-mha4s7stfa-uc.a.run.app/api/schema/redoc/)

## Running Tests

To run the backend tests, use the following command inside the backend container:

```bash
docker-compose exec backend python manage.py test
docker-compose exec frontend npm test
