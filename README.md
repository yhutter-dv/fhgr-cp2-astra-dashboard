<div align="center">
    <h1>:car: ASTRA Realtime Dashboard</h1> 
    <h2>Realtime Data Dashboard with ASTRA Dataset for Consultancy Project 2 @ FHGR</h2>
    <br/>
    <br/>
    <a href="https://github.com/yhutter-dv/fhgr-cp2-astra-dashboard/stargazers" target="_blank"><img alt="Stars" src="https://img.shields.io/github/stars/yhutter-dv/fhgr-cp2-astra-dashboard?color=191724&style=for-the-badge" /></a>
    <a href="https://github.com/yhutter-dv/fhgr-cp2-astra-dashboard/issues" target="_blank"><img alt="Issues" src="https://img.shields.io/github/issues/yhutter-dv/fhgr-cp2-astra-dashboard?color=191724&style=for-the-badge" /></a>
    <a href="https://mit-license.org" target="_blank"><img alt="License" src="https://img.shields.io/github/license/yhutter-dv/fhgr-cp2-astra-dashboard?color=191724&style=for-the-badge" /></a>
</div>

## :pencil2: Setup

### Clone the Repo
First of all clone this repository to a local destination of your choice
```bash
git clone https://github.com/yhutter-dv/fhgr-cp2-astra-dashboard.git ~/GitRepos/fhgr-cp2-astra-dashboard
```

### Backend 
The backend is implemented in Python. It is generally a good idea to create a virtual environment and install the required packages local to this environment:

```bash
cd backend
python -m venv ./.venv
source ./.venv/bin/active.sh
pip install -r ./requirements.txt
```

### Frontend
The frontend is written with React (Typescript) and the MUI Framework. First make sure that [NodeJS](https://nodejs.org/en/) is installed. If possible choose the **Current** Version.
After that simply install all required packages by running
```bash
cd frontend
npm i
```

## :rocket: Run the App
In order to run the App first start the backend and afterwards the frontend.

### Backend
```bash
uvicorn app:app --reload
```
In order to try out the Endpoints visit: `http://localhost:8000/docs`.

### Frontend
```bash
npm run dev
```

## Useful Links and Ressources

|Link|Description|
|-------|-----|
|[Why a .env?](https://blog.devgenius.io/why-a-env-7b4a79ba689)| Contains useful information what .env files are and how they can be used|
|[Open-Data-Plattform Mobilität Schweiz](https://opentransportdata.swiss/de/strassenverkehr/)| API in order to retrieve Realtime Data on Mobility related topics|
|[Make SOAP Requests](https://www.geeksforgeeks.org/making-soap-api-calls-using-python/)| How to make SOAP Requests in Python|
|[Speed up XML Parsing in Python](https://nickjanetakis.com/blog/how-i-used-the-lxml-library-to-parse-xml-20x-faster-in-python)| A good ressource for speeding up XML Parsing in Python|
|[Tailwind](https://tailwindcss.com/)| An awesome CSS Library |
|[VueJS](https://vuejs.org/)| A simple and fast progressive JavaScript Framework for building Single Page Applications|
|[MapLibreGL](https://maplibre.org/maplibre-gl-js/docs/)| A fast Map Library which uses WebGL for rendering|
|[MapLibreGL VueJs](https://github.com/razorness/vue-maplibre-gl)| Vue Wrapper around MapLibreGL|
|[Swisstopo Light Base Map](https://www.swisstopo.admin.ch/de/geodata/maps/smw/smw_lightbase.html)| A free to use Map from Swisstopo|
|[Apex Charts](https://apexcharts.com/)| An Chart Library with a modern look and feel|
|[FastAPI](https://github.com/tiangolo/fastapi)| A really fast REST API Library (pun intended) written in Python|
