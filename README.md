<div align="center">
    <h1>:car: ASTRA Realtime Dashboard</h1>
    <h2>Realtime Data Dashboard with ASTRA Dataset for Consultancy Project 2</h2>
    <br/>
    <br/>
</div>

## Clone the Repo

First of all clone this repository to a local destination of your choice

```bash
git clone https://github.com/yhutter-dv/fhgr-cp2-astra-dashboard.git ~/GitRepos/fhgr-cp2-astra-dashboard
```

## Fill out the .env file

In order for the Docker Container to work properly you need to fill out the
`.env` file in the `backend directory`.

## Scripts

In order to streamline some things we have created scripts. In order to use them
make sure they are executable, e.g

```bash
chmod +x *.sh
```

| Script                    | Purpose                                       |
| ------------------------- | --------------------------------------------- |
| run_influxdb.sh           | Starts and runs the InfluxDB Docker Container |
| run_docker.sh             | Starts all necessary Docker Containers        |
| clean_influxdb_storage.sh | Clean the entire influxdb storage             |

## :pencil2: Setup for Local Development

> Note that it is important that you start each component in the correct order
> as described below (e.g First InfluxDB then FastAPI and then Frontend).

### Influx DB

You can run Influx DB locally via Docker. For this simply execute the following
command or use the script `run_influxdb.sh`:

```bash
sudo docker compose up -d influxdb
```

InfluxDB should be available under this [URL](http://127.0.0.1:8086/).

### FastAPI

The backend is implemented in Python. It is generally a good idea to create a
virtual environment and install the required packages local to this environment:

```bash
cd backend
python -m venv ./.venv
source ./.venv/bin/active.sh
pip install -r ./requirements.txt
uvicorn app:app --reload
```

FastAPI should be available under this [URL](http://127.0.0.1:8000/docs).

> Be aware that the response contains about 2MB of JSON so trying it out inside
> Swagger may cause your browser to hang.

### Frontend

The Frontend is written in React (TypeScript) with some dependencies like
[React Map GL](https://visgl.github.io/react-map-gl/) and
[Apex Charts](https://apexcharts.com/). First make sure that
[NodeJS](https://nodejs.org/en/) is installed. If possible choose the
**Current** Version.

Also for the Map to work a
[MapBox Token](https://docs.mapbox.com/help/getting-started/access-tokens/) is
required. Once you have that you must add it to the `.env` in the frontend
diretory along with the URL of the FastAPI.

> :warning: Please do NOT check in the `.env` file with your Secrets.

After that simply install all required packages by running

```bash
cd frontend
npm i
npm run dev
```

## Jupyter Notebook

In order to explore the data in more depth we have created a Jupyter Notebook in
order to run it do the following commands:

```bash
cd jupyter_notebooks
python -m venv ./venv
source venv/bin/activate.sh
pip install -r requirements.txt
python -m ipykernel install --user --name=venv
jupyter notebook ./
```

Next a Browser Tab should open. Then you can select the Jupyter Notebook of your
choice.

> Important: Please do not forget to select the installed `venv` as the kernel
> in order to utilize the installed virtual environment in the Jupyter Notebook.

## :rocket: Setup for Deployment

In order to streamline the Deployment process we use
[Docker](https://docs.docker.com/engine/install/). Please make sure that it is
installed on your system and also that the `Docker Service is running`.

```bash
sudo systemctl start docker # Starts the docker service.
./run_docker.sh
```

After entering this command docker starts building the containers and pulling
down the necessary images. Please wait until this is completed.

### FastAPI

FastAPI should be available under this [URL](http://127.0.0.1:8000/docs).

### InfluxDB

InfluxDB should be available under this [URL](http://127.0.0.1:8086/).

## Used Ressources

| Link                                                                                                                           | Description                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| [Why a .env?](https://blog.devgenius.io/why-a-env-7b4a79ba689)                                                                 | Contains useful information what .env files are and how they can be used        |
| [Open-Data-Plattform Mobilität Schweiz](https://opentransportdata.swiss/de/strassenverkehr/)                                   | API in order to retrieve Realtime Data on Mobility related topics               |
| [Make SOAP Requests](https://www.geeksforgeeks.org/making-soap-api-calls-using-python/)                                        | How to make SOAP Requests in Python                                             |
| [Speed up XML Parsing in Python](https://nickjanetakis.com/blog/how-i-used-the-lxml-library-to-parse-xml-20x-faster-in-python) | A good ressource for speeding up XML Parsing in Python                          |
| [FastAPI](https://github.com/tiangolo/fastapi)                                                                                 | A really fast REST API Library (pun intended) written in Python                 |
| [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)                                                                    | Allow CORS in FastAPI                                                           |
| [FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)                                                           | How to setup FastAPI inside a Docker Container                                  |
| [InfluxDB in Docker](https://hub.docker.com/_/influxdb)                                                                        | How to setup InfluxDB inside a Docker Container                                 |
| [InfluxDB Python Client](https://github.com/influxdata/influxdb-client-python)                                                 | Sample Repo for working with InfluxDB and Python                                |
| [Svelte](https://svelte.dev/)                                                                                                  | A minimalistic JavaScript Framework with State Management and tiny Bundle Size. |
| [Heroicons](https://heroicons.com/)                                                                                            | Nice Icons designed by the makes of Tailwind                                    |
| [Leaflet](https://leafletjs.com/)                                                                                              | Tiny and efficient Map Library which does not require any Token.                |
| [Leaflet Swisstopo](https://leaflet-tilelayer-swiss.karavia.ch/)                                                               | Swisstopo support for Leaflet                                                   |
| [Apex Charts](https://apexcharts.com/)                                                                                         | Chart Library with lots of different chart types.                               |
| [Vite](https://vitejs.dev/guide/)                                                                                              | Super fast Web Bundler.                                                         |
| [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode)                                                            | How to use environment variables in Vite.                                       |
| [Tailwind CSS](https://tailwindcss.com/)                                                                                       | CSS Framework.                                                                  |
| [Tailwind CSS Forms](https://github.com/tailwindlabs/tailwindcss-forms)                                                        | A Tailwind inspired styling for Form Elements.                                  |
