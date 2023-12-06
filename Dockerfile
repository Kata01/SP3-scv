# Dockerfile
FROM alpine:latest

# Install FFmpeg
RUN apk --no-cache add ffmpeg

# Copy your Python script
COPY videotext.py /app/videotext.py

# Set working directory
WORKDIR /app

# Command to run the script
CMD ["python", "docker.py"]
