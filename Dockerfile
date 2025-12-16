FROM python:3.12-slim

# base working dir
WORKDIR /app

COPY fitness_tracker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy the project
COPY . /app/

WORKDIR /app/fitness_tracker

EXPOSE 8000

CMD ["bash", "-lc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
