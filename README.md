<div align="center">
    <h1>:car: ASTRA Realtime Dashboard</h1> 
    <h2>Realtime Data Dashboard with ASTRA Dataset for Consultancy Project 2 @ FHGR</h2>
    <br/>
    <br/>
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
The frontend is written in Vanilla Javascript with some dependencies like [ChartJS](https://www.chartjs.org/) and [Leaflet](https://leafletjs.com/). First make sure that [NodeJS](https://nodejs.org/en/) is installed. If possible choose the **Current** Version.
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

> Be aware that the response contains about 2MB of JSON so trying it out inside Swagger may cause your browser to hang.

### Frontend
```bash
npm run dev
```

## Useful Links and Ressources

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
