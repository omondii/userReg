# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Set environment variables for Flask and PostgreSQL
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
# Expose the port that Flask will run on
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run"]
