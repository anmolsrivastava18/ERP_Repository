docker-compose -f local.yml down
docker-compose -f local.yml up -d --force-recreate --no-dep --build postgres
docker-compose -f local.yml build --no-cache django

# remove local migrations
rm -rf aims/inventory/migrations aims/users/migrations

# Drop all the tables in the DB
docker-compose -f local.yml run --rm django python manage.py reset_db

docker-compose -f local.yml run --rm django python manage.py makemigrations

# Provide app names, sometimes app migrations not generating during `makemigrations`
docker-compose -f local.yml run --rm django python manage.py makemigrations users
docker-compose -f local.yml run --rm django python manage.py makemigrations inventory

docker-compose -f local.yml run --rm django python manage.py migrate
docker-compose -f local.yml run --rm django python manage.py createsuperuser


# Start the Django container Again
docker-compose -f local.yml up -d --force-recreate --no-dep --build django

# Populate the DB with the Fake Data
docker-compose -f local.yml run --rm django python populate_data.py

docker-compose -f local.yml logs -f django
