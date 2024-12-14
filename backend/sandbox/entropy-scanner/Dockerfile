# Start with a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for YARA Python bindings
RUN apt-get update

# Install the YARA Python bindings
RUN pip install EntropyAnalysis

# Copy your application files into the container
COPY . .

# Command to run your application (you can customize this as per your application logic)
CMD ["python", "entropy_scan.py"]
