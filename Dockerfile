# Use the official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install both runtime and testing dependencies
RUN pip install fastapi uvicorn pytest httpx

# Copy the FastAPI app and test script into the container
COPY main.py .
COPY test_main.py .

# Expose port 80 for HTTP traffic
EXPOSE 80

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
