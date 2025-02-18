# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . .

# Expose port 8000 (the default port for your FastAPI app)
EXPOSE 8000

# Run the FastAPI application using uvicorn.
# This command tells Uvicorn to use the "app" object from the module "app.app".
# It uses the PORT environment variable if set; otherwise, it defaults to 8000.
CMD ["sh", "-c", "uvicorn app.app:app --host 0.0.0.0 --port ${PORT:-8000}"]