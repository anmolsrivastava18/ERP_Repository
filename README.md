aims
====

Supply chain management system manage inwards, outwards and analytics of
Adonmob products/stocks.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)

[![ Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)



Deployment
----------
## Configure AWS CLI

```bash
export AWS_PROFILE=mani-per
export AWS_DEFAULT_REGION=us-east-2
# if this env var is not set use the flag with `--profile`  with every aws cli command. 

aws configure # provide the aws_access_key_id and aws_secret_access_keys

```



## Configuring RDS Postgres

Create RDS Postgres with Public access enabled

```bash
psql postgres://postgres:DB_super_secret_password@database-2.crp58bgdc8hz.us-east-2.rds.amazonaws.com:5432

postgres=> CREATE DATABASE aims;


```



## Configuring S3

```bash
aws s3 mb s3://aims-staticfiles --region us-east-2

```

## Configure S3 CORS for buckets


```xml
<CORSConfiguration>
	<CORSRule>
		<AllowedOrigin>*</AllowedOrigin>
		<AllowedMethod>GET</AllowedMethod>
	</CORSRule>
</CORSConfiguration>
```


## Building web app image and ECR


Create a repository in ECR console and copy the repo URI. ex: 541300190783.dkr.ecr.us-east-2.amazonaws.com/aims

- Authenticate/configure ECR credentials with `docker login`

```bash
aws ecr get-login --region us-east-2 --no-include-email

```


- Build docker image and push to ECR
```bash
docker build --no-cache -t 541300190783.dkr.ecr.us-east-2.amazonaws.com/aims:dev-01 -f ./compose/production/django/Dockerfile .

docker push 541300190783.dkr.ecr.us-east-2.amazonaws.com/aims:dev-01

```


## Try Running container locally with remote DB

### Environmental variables the container uses

```bash
# if this is set, collect static will not be run, saves lot time during deployment without changes.
DONT_RUN_COLLECT_STATIC=True
PORT=5000
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=opZdgD9XUtAU4qrYQMk3wG5HyAvWKXiTUaGWxMPokb7d9wpN1vgtoGWSKA8yEps7
DJANGO_ADMIN_URL=aims-admin/
DJANGO_ALLOWED_HOSTS="*"
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
DJANGO_AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
DJANGO_AWS_STORAGE_BUCKET_NAME=aims-staticfiles
DJANGO_AWS_S3_REGION_NAME=us-east-2
WEB_CONCURRENCY=4
POSTGRES_HOST=database-2.crp58bgdc8hz.us-east-2.rds.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_DB=aims
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
```


```bash


# Create schema in DB

docker run --rm -it --rm --env-file .envs/.production/.django  541300190783.dkr.ecr.us-east-2.amazonaws.com/aims:dev-01 python manage.py migrate
docker run --rm -it --rm --env-file .envs/.production/.django  541300190783.dkr.ecr.us-east-2.amazonaws.com/aims:dev-01 python manage.py createsuperuser

docker run --rm -it -p 80:5000  --env-file .envs/.production/.django  541300190783.dkr.ecr.us-east-2.amazonaws.com/aims:dev-01 /start


```





Settings
--------

Moved to
[settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you'll see a "Verify Your E-mail
    Address" page. Go to your console to see a simulated email
    verification message. Copy the link into your browser. Now the
    user's email should be verified and ready to go.
-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.


### Creating Assets with out Outwarding the Parts Used in the BOM. 
- 	Provide the following values in the same format

```
$ python manage.py create_assets <BOMName> <Quantity> <ProductName> <WarehouseName> <MFGDate> <Remarks>
```

- 	Note: 

### For Force Calculating the Average Price's of the Parts. 

```
$ python manage.py average_price
```
-	Note:- Schedule Job will run to calculate the Average Prices of all the part's everyday 11:00 PM

Deployment
----------

The following details how to deploy this application.

### With Docker compose

See detailed [cookiecutter-django Docker
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

