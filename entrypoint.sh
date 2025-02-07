#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Происходит минификация CSS-файлов..."
for file in /var/www/static/css/*.css; do
    uglifycss "$file" > temp.css
    mv temp.css "$file"
    echo "Файл $file минифицирован"
done

echo "Происходит минификация JS-файлов..."
for file in /var/www/static/js/*.js; do
    uglifyjs "$file" --compress --mangle -o "$file"
    echo "Файл $file минифицирован"
done

celery -A core worker -l info -P prefork &
celery -A core beat -l info &
celery -A core flower -l info &
gunicorn core.wsgi:application --bind 0.0.0.0:8000 &

wait