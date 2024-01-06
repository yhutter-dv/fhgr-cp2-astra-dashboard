import './app.css'
import "leaflet/dist/leaflet.css";

import Dashboard from './Dashboard.svelte'

const dashboard = new Dashboard({
  target: document.getElementById('dashboard'),
})

export default dashboard
