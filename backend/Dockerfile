# docker run --rm my-app-image /path/to/your-executable

# Use a minimal base image with necessary utilities
FROM alpine:latest

# Set the working directory in the container
WORKDIR /app

# Start a shell, execute the binary from the command line, and then run ps
CMD sh -c "$1 && ps aux >> /tmp/output"
