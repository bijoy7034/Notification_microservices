# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables (optional defaults)
ENV PYTHONUNBUFFERED=1

# Run the email service
CMD ["python", "-m", "app.main"]
