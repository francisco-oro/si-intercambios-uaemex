# si-intercambios-uaemex
Sistema de intercambios - UAEMéx

# Development Setup 

## Getting Started - Perform & Apply migrations 
```shell
docker compose run --rm backend sh -c "python manage.py make migrations && python manage.py migrate"
```

## Getting Started - CreateSuperuser
```shell
docker compose run --rm -it backend sh -c "python manage.py createsuperuser"
```

Now, head to `0.0.0.0:8000` and provide your credentials to log-in

## Launch backend + PostgreSQL database
```shell
docker compose up 
```

## Launch frontend
```shell
cd si-uaemex-frontend/
npm install
ng serve -o
```

Head to `localhost:3000` in your browser to display the frontend app


# Testing

```shell
docker compose run --rm backend sh -c "python manage.py test"
```
# Linting

```shell
docker compose run --rm backend sh -c "flake8"
```


# Production Setup

This is the last change to be reflected