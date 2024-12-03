# Use a Python base image
FROM python:3.13

# Install Redis
RUN apt-get update && \
    apt-get install -y redis-server

# Set the working directory
WORKDIR /app

# Copy the app files into the container
COPY . .

# Install dependencies (like FastAPI, Redis Python client, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI default port
EXPOSE 8080

# Expose Redis port
EXPOSE 6379

# Start Redis in the background and then start FastAPI app with uvicorn
CMD redis-server --daemonize yes && uvicorn main:app --host 0.0.0.0 --port 8080