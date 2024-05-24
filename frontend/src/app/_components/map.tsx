import {MapContainer, TileLayer, Marker, Popup} from 'react-leaflet';
import React from "react";
import {styled} from "styled-components";

interface MapProps {
    searched: boolean;
    markers: { lat: number, lng: number }[];
}

const MapWrapper = styled.div`
    height: 500px;
`;

export const Map = (props: MapProps) => {
    return (
        <MapWrapper>
            <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[51.505, -0.09]}>
                    <Popup>
                        A pretty CSS3 popup. <br/> Easily customizable.
                    </Popup>
                </Marker>
            </MapContainer>
        </MapWrapper>
    );
}