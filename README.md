# si-intercambios-uaemex
Sistema de intercambios - UAEMéx

# Development Setup 

## Getting Started - Perform & Apply migrations 
```shell
docker compose run app-db --rm sh -c "python manage.py make migrations && python manage.py migrate"
```

## Getting Started - CreateSuperuser
```shell
docker compose run app-db --rm -it sh -c "python manage.py createsuperuser"
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
# Production Setup