FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py /app/app.py

# Install dependencies
RUN pip install flask

# Expose port
EXPOSE 6000

# Run the application
CMD ["python", "app.py"]

