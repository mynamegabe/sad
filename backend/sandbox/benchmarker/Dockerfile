# docker run --rm my-app-image /path/to/your-executable

# Use a minimal base image with necessary utilities
FROM alpine:latest

# Set the working directory in the container
WORKDIR /app

COPY benchmark.sh benchmark.sh

COPY ls_mainexe ls_mainexe
COPY run.sh run.sh

# Start a shell, execute the binary from the command line, and then run ps
# CMD sh -c "./run.sh $1"
CMD ls & ./benchmark.sh
