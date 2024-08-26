mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
admin:
	python3 manage.py createsuperuser
app:
	python3 manage.py startapp apps
run:
	python3 manage.py runserver
shell:
	python manage.py shell
redis:
	sudo systemctl start redis-server
celery:
	celery -A root worker --loglevel=info
stop-redis:
	sudo systemctl stop redis
stop-celery:
	pkill -f 'celery worker'
flower:
	celery -A root.celery.app flower --port=5555
fixture-product:
	python manage.py dumpdata apps.Product --output=apps/fixtures/Product.json
fixture-category:
	python manage.py dumpdata apps.Product --output=apps/fixtures/Category.json
load-category:
	python manage.py loaddata Category.json
load-product:
	python manage.py loaddata Product.json