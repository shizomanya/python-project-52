# Use the official Python image from the Docker Hub
# with Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

## Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app/

EXPOSE 8000