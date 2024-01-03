// Implemented with reference to https://visgl.github.io/react-map-gl/examples/controls
import { useMemo, useState } from 'react';
import Map, {
  Marker,
  FullscreenControl,
  GeolocateControl,
  Popup,
} from 'react-map-gl';
import { Station } from '../models/Station';
import { StationMarker } from '../models/StationMarker';
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/solid';

type Props = {
  stations: Array<Station>
}


export default function MapLibreStationMap({ stations }: Props) {

  const TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;
  const STYLE = "mapbox://styles/mapbox/streets-v12";

  const STATIONS: Array<Station> = [
    {
      latitude: 47.36667,
      longitude: 8.55,
      name: "Zürich",
      numberOfErrors: 0
    },
    {
      latitude: 46.947456,
      longitude: 7.451123,
      name: "Bern",
      numberOfErrors: 10
    }
  ];

  const MARKERS = STATIONS.map(s => createStationMarker(s));

  function createStationMarker(station: Station): StationMarker {
    return {
      station,
      active: false
    };
  }

  const [popupInfo, setPopupInfo] = useState<Station | undefined>(undefined);
  const [stationMarkers, setStationMarkers] = useState<Array<StationMarker>>(MARKERS);

  const iconForMarker = (marker: StationMarker) => {
    if (marker.station.numberOfErrors > 0) {
      return (
        <div className='p-1 bg-white rounded-full'>
          <ExclamationCircleIcon className={marker.active === true ? "h-8 w-8 text-black" : "h-8 w-8 text-red-500"} />
        </div>
      )
    }
    return (
      <div className='p-1 bg-white rounded-full'>
        <CheckCircleIcon className={marker.active === true ? "h-8 w-8 text-black" : "h-8 w-8 text-green-500"} />
      </div>
    )
  }

  const pins = useMemo(
    () =>
      stationMarkers.map((marker, index) => (
        <Marker
          key={`marker-${index}`}
          longitude={marker.station.longitude}
          latitude={marker.station.latitude}
          anchor="bottom"
          onClick={e => {
            e.originalEvent.stopPropagation();

            // Set only the clicked station as active and the other as inactive.
            stationMarkers.forEach(m => m.active = m.station.name === marker.station.name);
            setStationMarkers([...stationMarkers]);
            setPopupInfo(marker.station);
          }}
        >
          {
            iconForMarker(marker)
          }
        </Marker>
      )),
    [stationMarkers]
  );

  return (
    <>
      <Map
        initialViewState={{
          latitude: 46.94809,
          longitude: 8.55,
          zoom: 7.0,
          bearing: 0,
          pitch: 0
        }}
        mapStyle={STYLE}
        mapboxAccessToken={TOKEN}
      >
        <GeolocateControl position="top-left" />
        <FullscreenControl position="top-left" />
        {pins}

        {popupInfo && (
          <Popup
            className='p-4'
            closeButton={false}
            anchor="top"
            longitude={popupInfo.longitude}
            latitude={popupInfo.latitude}
            onClose={() => setPopupInfo(undefined)}
          >
            <div>
              <h1 className=''>{popupInfo.name}</h1>
            </div>
          </Popup>
        )}
      </Map>
    </>
  );
}