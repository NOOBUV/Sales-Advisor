# Build stage for client
FROM node:22 as client_build

WORKDIR /app/client
COPY client/package.json client/package-lock.json ./
RUN npm install
COPY client .
RUN npm run build

# Production stage
FROM python:3.12.3

WORKDIR /app

# Copy requirements and install dependencies
COPY server/requirements.txt .
RUN pip install gunicorn whitenoise
RUN pip install -r requirements.txt

# Copy the server code
COPY server /app

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/templates

# Copy the built client files
COPY --from=client_build /app/client/dist /app/static
COPY --from=client_build /app/client/dist/index.html /app/templates/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "salesAdvisor.wsgi:application"]