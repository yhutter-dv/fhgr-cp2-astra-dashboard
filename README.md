<div align="center">
    <h1>:car: ASTRA Realtime Dashboard</h1> 
    <h2>Realtime Data Dashboard with ASTRA Dataset for Consultancy Project 2 @ FHGR</h2>
    <br/>
    <br/>
</div>

## Clone the Repo
First of all clone this repository to a local destination of your choice
```bash
git clone https://github.com/yhutter-dv/fhgr-cp2-astra-dashboard.git ~/GitRepos/fhgr-cp2-astra-dashboard
```

## Scripts
In order to streamline some things we have created scripts. In order to use them make sure they are executable, e.g
```bash
chmod +x run_influx_local.sh
...
```

|Script|Purpose|
|---|------|
|run_influx_local.sh|Starts and runs the InfluxDB Docker Container locally using `.env-local` as the environment file|
|run_docker_local.sh|Starts all necessary Docker Containers locally using the `.env-local` as the environment file|
|run_docker_prod.sh|Meant for production. Please make sure that you have filled out all fields in the `.env` file.|

## :pencil2: Setup for Local Development

### FastAPI
The backend is implemented in Python. It is generally a good idea to create a virtual environment and install the required packages local to this environment:

```bash
cd backend
python -m venv ./.venv
source ./.venv/bin/active.sh
pip install -r ./requirements.txt
uvicorn app:app --reload
```

FastAPI should be available under this [URL](http://127.0.0.1:8000/docs).

> Be aware that the response contains about 2MB of JSON so trying it out inside Swagger may cause your browser to hang.

### Frontend
The frontend is written in Vanilla Javascript with some dependencies like [ChartJS](https://www.chartjs.org/) and [Leaflet](https://leafletjs.com/). First make sure that [NodeJS](https://nodejs.org/en/) is installed. If possible choose the **Current** Version.
After that simply install all required packages by running
```bash
cd frontend
npm i
npm run dev
```

### Influx DB
You can run Influx DB locally via Docker. For this simply execute the following command:
```bash
sudo docker compose --env-file backend/.env-local up -d influxdb
```
InfluxDB should be available under this [URL](http://127.0.0.1:8086/).

## Jupyter Notebook
In order to explore the data in more depth we have created a Jupyter Notebook in order to run it do the following commands:
```bash
cd jupyter_notebooks
python -m venv ./venv
source venv/bin/activate.sh
pip install -r requirements.txt
python -m ipykernel install --user --name=venv
jupyter notebook ./
```

Next a Browser Tab should open. Then you can select the Jupyter Notebook of your choice.

> Important: Please do not forget to select the installed `venv` as the kernel in order to utilize the installed virtual environment in the Jupyter Notebook.

## :rocket: Setup for Deployment
In order to streamline the Deployment process we use [Docker](https://docs.docker.com/engine/install/). Please make sure that it is installed on your system and also that the `Docker Service is running`.
Also make sure that the `docker-compose` command is available.

```bash
sudo docker-compose up -d --build
```
After entering this command docker starts building the containers and pulling down the necessary images. Please wait until this is completed.

### FastAPI
FastAPI should be available under this [URL](http://127.0.0.1:8000/docs).

### InfluxDB
InfluxDB should be available under this [URL](http://127.0.0.1:8086/).

## Used Ressources

|Link|Description|
|--|----|
|[Why a .env?](https://blog.devgenius.io/why-a-env-7b4a79ba689)| Contains useful information what .env files are and how they can be used|
|[Open-Data-Plattform Mobilität Schweiz](https://opentransportdata.swiss/de/strassenverkehr/)| API in order to retrieve Realtime Data on Mobility related topics|
|[Make SOAP Requests](https://www.geeksforgeeks.org/making-soap-api-calls-using-python/)| How to make SOAP Requests in Python|
|[Speed up XML Parsing in Python](https://nickjanetakis.com/blog/how-i-used-the-lxml-library-to-parse-xml-20x-faster-in-python)| A good ressource for speeding up XML Parsing in Python|
|[Swisstopo Light Base Map](https://www.swisstopo.admin.ch/de/geodata/maps/smw/smw_lightbase.html)| A free to use Map from Swisstopo|
|[FastAPI](https://github.com/tiangolo/fastapi)| A really fast REST API Library (pun intended) written in Python|
|[Gnome Human Interface Guidelines](https://developer.gnome.org/hig/)| Design inspiration for look and feel of the dashboard|
|[FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)| Allow CORS in FastAPI|
|[Leaflet](https://leafletjs.com/)| Simple and fast Map Library |
|[FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)| How to setup FastAPI inside a Docker Container |
|[InfluxDB in Docker](https://hub.docker.com/_/influxdb)| How to setup InfluxDB inside a Docker Container |
