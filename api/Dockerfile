# Use the official Python image as the base image
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Set environment variables for testing
ENV DATABASE_URL=sqlite:///:memory:
ENV PYTHONPATH=/app

# Expose the port that Flask will run on
EXPOSE 5000

# Start the Flask application
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
