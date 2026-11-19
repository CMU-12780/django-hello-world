FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Create the database and load the starter facts, then serve on all interfaces
CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata facts && python manage.py runserver 0.0.0.0:8000"]
