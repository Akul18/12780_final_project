FROM python:3.12-slim

# base working dir
WORKDIR /app

# copy requirements first (better caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy your whole project
COPY . /app/

# move into the folder that contains manage.py
WORKDIR /app/fitness_tracker

EXPOSE 8000

# run migrations then start server (bind to 0.0.0.0 so host can reach it)
CMD ["bash", "-lc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
