# Dockerfile

# Use the official lightweight Python image.
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src:app"]
