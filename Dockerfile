FROM python:3.10

# Disables writing bytecode files, potentially improving performance.
ENV PYTHONDONTWRITEBYTECODE=1
# Enables unbuffered output for standard streams.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y nodejs npm

# Copy the entire project
COPY . /app/

# Install Python dependencies
WORKDIR /app/server
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Install and build React app
WORKDIR /app/client
RUN npm install 
RUN npm run build

# Create static directory and copy built React app
WORKDIR /app/server
RUN mkdir -p salesAdvisor/static
RUN cp -r /app/client/dist/* salesAdvisor/static/

# Collect static files
WORKDIR /app/server
RUN python manage.py collectstatic --noinput

# Run the application
CMD ["gunicorn", "salesAdvisor.wsgi:application", "--bind", "0.0.0.0:8000"]