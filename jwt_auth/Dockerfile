# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy the app files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI default port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]