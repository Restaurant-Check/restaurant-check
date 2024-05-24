"use client";

import {MapContainer, TileLayer, Marker} from 'react-leaflet';
import React from "react";
import {styled} from "styled-components";
import {Box} from "@/app/_components/box";

interface MapProps {
  searched: boolean;
  markers: { lat: number, lng: number }[];
}

const MapWrapper = styled.div`
    height: 500px;
`;

export const MapComponent = (props: MapProps) => {
  return (
    <Box searched={props.searched}>
      <MapWrapper>
        <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={[51.505, -0.09]}>
          </Marker>
        </MapContainer>
      </MapWrapper>
    </Box>
  );
}