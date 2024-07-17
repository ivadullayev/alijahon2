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


