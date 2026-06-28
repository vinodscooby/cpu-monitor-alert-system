FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (including app folder)
COPY . .

EXPOSE 8080

CMD ["python", "-m", "app.main"]