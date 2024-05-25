"use client";

import {MapContainer, TileLayer, Marker, Popup, useMap} from 'react-leaflet';
import React, {useEffect} from "react";
import {styled} from "styled-components";
import {Box} from "@/app/_components/box";
import {Icon, LatLngBounds, Point} from "leaflet";
import {Restaurant} from "@/app/page";
import {Button} from "@mantine/core";

interface MapProps {
    searched: boolean;
    restaurants: Restaurant[];
    hoveringOver: number;
    setLocateRestaurant: React.Dispatch<React.SetStateAction<(index: number) => void>>;
}

interface ResetViewButtonProps {
    bounds: LatLngBounds;
    boundOptions: {
        paddingTopLeft: Point;
        paddingBottomRight: Point;
    };
    props: MapProps;
    scrolled: boolean;
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

const MapWrapper = styled.div<{ $searched: boolean, $scrolled: boolean }>`
    overflow: hidden;
    border-radius: var(--mantine-radius-lg);
    ${props => props.$searched && `z-index: 1000;`}
    height: ${props => props.$scrolled ? '200px' : '500px'};
    transition: height 0.2s;
`;

const Map = styled(MapContainer)`
    height: 100vh;
    width: 100vw;
`;

const InvisibleBox = styled.div`
    position: absolute;
    top: 188px;
    height: 500px;
    width: 100%;
    visibility: hidden;
`;

const ResetViewButton = ({bounds, boundOptions, props, scrolled}: ResetViewButtonProps) => {
    const map = useMap();

    const handleResetView = () => {
        map.flyToBounds(bounds, boundOptions);
    };

    const flyToRestaurant = (index: number) => {
        const restaurant = props.restaurants[index];
        const coordinates = {
            lat: restaurant.coordinates[0],
            lng: restaurant.coordinates[1]
        };
        map.flyToBounds(new LatLngBounds(coordinates, coordinates), {...boundOptions, maxZoom: 13});
    };

    useEffect(() => {
        props.setLocateRestaurant(() => flyToRestaurant);
    }, [scrolled, props]);

    useEffect(() => {
        handleResetView()
    }, [props.restaurants]);

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
    if (props.restaurants.length === 0) {
        return <Box
            $searched={props.searched}
            style={
                {
                    zIndex: props.searched ? 999 : -1,
                    height: "542px",
                    backgroundColor: '#242424',
                }
            }
        ><></>
        </Box>
    }
    let bounds = new LatLngBounds(props.restaurants[0].coordinates, props.restaurants[0].coordinates);
    props.restaurants.forEach(restaurant => bounds.extend(restaurant.coordinates));
    const [scrolled, setScrolled] = React.useState(false);
    const boundOptions = {
        paddingTopLeft: new Point((-window.innerWidth * 0.1), (scrolled ? (-200) : 50)),
        paddingBottomRight: new Point(window.innerWidth * 0.2, window.innerHeight * 0.5),
        duration: 0.8
    }

    React.useEffect(() => {
        const mapElement = document.getElementById('map');
        if (!mapElement) {
            return;
        }
        const checkScroll = () => {
            const rect = mapElement.getBoundingClientRect();
            if (rect.top == 16) {
                setScrolled(true);
            } else {
                setScrolled(false)
            }
        };

        window.addEventListener('scroll', checkScroll);

        return () => {
            window.removeEventListener('scroll', checkScroll);
        };
    }, []);

    return (
        <>
            <InvisibleBox/>
            <Box
                $searched={props.searched}
                id={'map'}
                style={
                    {
                        position: 'sticky',
                        top: '16px',
                        zIndex: props.searched ? 999 : -1,
                        height: scrolled ? '242px' : "542px",
                        backgroundColor: '#242424',
                    }
                }
            >
                <MapWrapper $searched={props.searched} $scrolled={scrolled}>
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
                        <ResetViewButton bounds={bounds} boundOptions={boundOptions} props={props} scrolled={scrolled}/>
                    </Map>
                </MapWrapper>
            </Box>
        </>
    );
}