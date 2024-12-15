# Start with a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for YARA Python bindings
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libmagic-dev \
    yara

# Install the YARA Python bindings
RUN pip install yara-python 

# Copy your application files into the container
COPY . .
RUN python yara_main.py --update

# Command to run your application (you can customize this as per your application logic)
CMD ["python", "yara_main.py","--scan-dir", "/app/testdir", "--gen-report"]
