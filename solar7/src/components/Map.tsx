// Map.tsx
import React from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const Map = () => {
    const mapStyles = {
        height: '100vh',
        width: '100%',
      };
  // Handle marker click event to fetch data from another Google Maps API using the coordinates.

    const defaultCenter = {
      lat: 37.7749, // Replace with your desired latitude
      lng: -122.4194, // Replace with your desired longitude
  };

  return (
    <LoadScript googleMapsApiKey="AIzaSyDquwjG9pbEcD56YGyRwmzvmbotq797F1c">
      <GoogleMap
        mapContainerStyle={mapStyles}
        zoom={10}
        center={defaultCenter}
      >
        <Marker
          position={{ lat: 0, lng: 0 }} // Initial marker coordinates
        />
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
