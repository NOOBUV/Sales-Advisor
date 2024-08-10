https://www.loom.com/share/73f6b76d4ffe41a284eae9a23db224f6
# SalesAdvisor

SalesAdvisor is a comprehensive solution designed to assist sales organizations in managing and analyzing their sales data effectively. The platform offers various features including user management, role-based access control, and insightful analytics to help improve sales performance.

Currently i'm using csv as mock database, but we can also maintain a database of several org's databases which can be queried upon.

## Features

- User Registration and Login with Google Single Sign-On
- Role-Based Access Control
- Sales Data Querying and Analytics
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

- Whole application is packaged using whitenoise so if you run docker (backend and frontend will be served on port 8000)
- The backend API will be available at [https://localhost:8000/api](https://localhost:8000/api)
- The frontend will be available at [http://localhost:5713](http://localhost:5713)

## API Documentation

API documentation is available via DRF Spectacular. Access the following endpoints to view the documentation:

- **Schema**: [https://localhost:8000/api/schema](https://localhost:8000/api/schema)
- **Swagger UI**: [https://localhost:8000/api/swagger-ui](https://localhost:8000/api/swagger-ui)
- **Redoc**: [https://localhost:8000/api/redoc](https://localhost:8000/api/redoc)

## Running Tests

To run the backend tests, use the following command inside the server container:

