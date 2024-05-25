"use client";

import {MapContainer, TileLayer, Marker, Popup, useMap} from 'react-leaflet';
import React from "react";
import {styled} from "styled-components";
import {Box} from "@/app/_components/box";
import {Icon, LatLngBounds, Point} from "leaflet";
import {Restaurant} from "@/app/page";
import {Button} from "@mantine/core";

interface MapProps {
    searched: boolean;
    restaurants: Restaurant[];
    hoveringOver: number;
}

interface ResetViewButtonProps {
    bounds: LatLngBounds;
    boundOptions: {
        paddingTopLeft: Point;
        paddingBottomRight: Point;
    };
}

const customMarkerIcon = new Icon({
    iconUrl: 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/map-marker-512.png',
    iconSize: [40, 40],
    iconAnchor: [20, 41],
    popupAnchor: [0, -40],
    shadowSize: [41, 41]
});

const customMarkerIconHover = new Icon(
    {
        iconUrl: 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/map-marker-512.png',
        iconSize: [50, 50],
        iconAnchor: [25, 51],
        popupAnchor: [0, -40],
        shadowSize: [41, 41]
    }
);

const MapWrapper = styled.div<{ $searched: boolean }>`
    height: 500px;
    overflow: hidden;
    border-radius: var(--mantine-radius-lg);
    transition: height 0.5s;
    ${props => props.$searched && `z-index: 1000;`}
`;

const Map = styled(MapContainer)`
    height: 100vh;
    width: 100vw;
`;

const ResetViewButton = ({bounds, boundOptions}: ResetViewButtonProps) => {
    const map = useMap();

    const handleResetView = () => {
        map.flyToBounds(bounds, boundOptions);
    };

    return (
        <div style={{position: 'absolute', top: '455px', left: '10px', zIndex: 500}}>
            <Button
                onClick={handleResetView}
                radius={'lg'}
                variant={'default'}
            >
                Reset View
            </Button>
        </div>
    );
};

export const MapComponent = (props: MapProps) => {
    let bounds = new LatLngBounds(props.restaurants[0].coordinates, props.restaurants[0].coordinates);
    props.restaurants.forEach(restaurant => bounds.extend(restaurant.coordinates));
    const boundOptions = {
        paddingTopLeft: new Point(0, 50),
        paddingBottomRight: new Point(window.innerWidth * 0.2, window.innerHeight * 0.5)
    }


    return (
        <Box $searched={props.searched}>
            <MapWrapper $searched={props.searched}>
                <Map
                    scrollWheelZoom={false}
                    bounds={bounds}
                    boundsOptions={
                        boundOptions
                    }
                >
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png"
                    />
                    {props.restaurants.map((restaurant, index) => (
                        <Marker
                            key={index}
                            position={restaurant.coordinates}
                            icon={index === props.hoveringOver ? customMarkerIconHover : customMarkerIcon}
                        >
                            <Popup>
                                {restaurant.name}
                            </Popup>
                        </Marker>
                    ))}
                    <ResetViewButton bounds={bounds} boundOptions={boundOptions}/>
                </Map>
            </MapWrapper>
        </Box>
    );
}