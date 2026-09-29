#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "▶ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "▶ Collecting static files..."
python manage.py collectstatic --no-input

echo "▶ Running migrations..."
python manage.py migrate --no-input

echo "▶ Loading fixture if database is empty..."
python manage.py shell -c "
from apps.testing.models import Question
if Question.objects.count() == 0:
    from django.core.management import call_command
    call_command('loaddata', 'apps/testing/fixtures/questions.json')
    print(f'Loaded {Question.objects.count()} questions')
else:
    print(f'Questions already present: {Question.objects.count()}')
"

echo "▶ Build complete."