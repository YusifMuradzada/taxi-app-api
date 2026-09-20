import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import L from "leaflet";

import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

const defaultIcon = L.icon({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

type Location = {
  latitude: number;
  longitude: number;
};

type MapProps = {
  pickup: Location | null;
  destination: Location | null;
  onPickupSelect: (
    latitude: number,
    longitude: number
  ) => void;
  onDestinationSelect: (
    latitude: number,
    longitude: number
  ) => void;
};

function MapClick({
  pickup,
  destination,
  onPickupSelect,
  onDestinationSelect,
}: MapProps) {
  useMapEvents({
    click(event) {
      const latitude = event.latlng.lat;
      const longitude = event.latlng.lng;

      if (!pickup) {
        onPickupSelect(latitude, longitude);
        return;
      }

      if (!destination) {
        onDestinationSelect(latitude, longitude);
        return;
      }
    },
  });

  return null;
}

function Map({
  pickup,
  destination,
  onPickupSelect,
  onDestinationSelect,
}: MapProps) {
  const defaultPosition: [number, number] = [
    40.4093,
    49.8671,
  ];

  return (
    <MapContainer
      center={defaultPosition}
      zoom={13}
      className="map-container"
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MapClick
        pickup={pickup}
        destination={destination}
        onPickupSelect={onPickupSelect}
        onDestinationSelect={onDestinationSelect}
      />

      {pickup && (
        <Marker
          position={[
            pickup.latitude,
            pickup.longitude,
          ]}
          icon={defaultIcon}
        >
          <Popup>
            📍 Pickup location
          </Popup>
        </Marker>
      )}

      {destination && (
        <Marker
          position={[
            destination.latitude,
            destination.longitude,
          ]}
          icon={defaultIcon}
        >
          <Popup>
            🏁 Destination
          </Popup>
        </Marker>
      )}
    </MapContainer>
  );
}

export default Map;