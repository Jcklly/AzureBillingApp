# ==== Build Backend ====
FROM python:3.9 AS backend-build
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# ==== Build Frontend ====
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ .
RUN npm run build

# ==== Final Stage: Combined Image ====
FROM ubuntu:20.04

# Set non-interactive mode to prevent timezone selection prompt
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && \
    apt-get install -y supervisor nginx python3 python3-pip tzdata curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copy the backend and frontend
COPY --from=backend-build /app/backend /app/backend
COPY --from=frontend-build /app/frontend/build /var/www/html

# Install Python dependencies inside the final image
RUN pip3 install --no-cache-dir -r /app/backend/requirements.txt

# Copy Supervisor configuration
COPY supervisor.conf /etc/supervisor/conf.d/supervisord.conf

# Set working directory to backend
WORKDIR /app/backend

# Expose ports
EXPOSE 80 8000

# Start Supervisor (which will run both uvicorn and nginx)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]