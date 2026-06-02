FROM python:3.12-slim

WORKDIR /app

COPY src ./src
COPY static ./static

ENV HOST=0.0.0.0
ENV PORT=8080
ENV MOCK_MODE=true

EXPOSE 8080

CMD ["python", "src/server.py"]
