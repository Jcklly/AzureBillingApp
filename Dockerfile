# ==== Build Backend ====
FROM python:3.9 AS backend-build
WORKDIR /app/backend
# Copy backend requirements and install them
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy backend code
COPY backend/ .

# ==== Build Frontend ====
FROM node:18 AS frontend-build
WORKDIR /app/frontend
# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
# Copy the rest of the frontend code and build it
COPY frontend/ .
RUN npm run build

# ==== Final Stage: Combined Image ====
FROM ubuntu:20.04

# Set non-interactive mode to prevent timezone selection prompt
ENV DEBIAN_FRONTEND=noninteractive

# Install needed packages: supervisor, nginx, python3, and pip
RUN apt-get update && \
    apt-get install -y supervisor nginx python3 python3-pip tzdata && \
    rm -rf /var/lib/apt/lists/*

# Create directories for logs if needed
RUN mkdir -p /var/log/uvicorn /var/log/nginx

# Copy the backend code from the backend-build stage
COPY --from=backend-build /app/backend /app/backend

# Copy the frontend build from the frontend-build stage into nginx’s default html folder
RUN rm -rf /var/www/html/*
COPY --from=frontend-build /app/frontend/build /var/www/html

# Copy your Supervisor configuration file
COPY supervisor.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port 80 (nginx) – this will be the port your App Service listens on
EXPOSE 80

# Start Supervisor (which will run both uvicorn and nginx)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]