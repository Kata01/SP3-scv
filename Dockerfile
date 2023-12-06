FROM alpine:latest

RUN apk --no-cache add ffmpeg

COPY videotext.py /app/main.py

WORKDIR /app

CMD ["python", "docker.py"]
