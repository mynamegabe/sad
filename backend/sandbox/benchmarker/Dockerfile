# docker run --rm my-app-image /path/to/your-executable

# Use a minimal base image with necessary utilities
# FROM alpine:latest
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

COPY benchmark.sh benchmark.sh

COPY run.sh run.sh

# Start a shell, execute the binary from the command line, and then run ps
CMD sh -c "./run.sh $1"
