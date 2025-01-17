# Devgrid Challenge

## Setup

1. How to run the project:

 - Create a virtual environment and install the dependencies:
```bash
git clone <repository_url>
cd devgrid_challenge

python -m venv .venv

cp ./app/.env.example ./app/.env

make setup

````
 - Note that fastapi app is running on port 8000 and the database is running on port POSTGRES_PORT in ./app/.env. If you have any service running on these ports, you can change the ports in the docker-compose.yml file.

 - Fill the .env file with the correct values and remeber to update WEATHER_API_KEY (see for more information: https://openweathermap.org/api/one-call-3)

- Build containers project and run the migrations:

```bash
make build

make migrate

make upgrade

````

2. How to run the tests:
```bash
make tests
```

3. If you want to debug the project: 

- You can see all docker logs with this dashboard
   
```bash
make log
```

4. FastApi Documentation:
http://localhost:8000/docs

