'use client'

import {Searchbar} from "@/app/_components/searchbar";
import {List} from "@/app/_components/list";
import {styled, StyleSheetManager} from "styled-components";
import React, {useState} from "react";
import dynamic from "next/dynamic";
import {fetchRestaurants} from "@/app/api";

const MapComponent = dynamic(
    () => import('@/app/_components/mapComponent').then(mod => mod.MapComponent),
    {ssr: false}
)

const PageContainer = styled.main`
    width: 100vw;
`;

const ContentContainer = styled.div`
    position: absolute;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    top: 168px;
    flex-direction: column;
`;

export interface Restaurant {
    name: string;
    rating: number;
    distance: string;
    closingTime: string;
    highlights: string[];
    coordinates: [number, number];
}

export default function Home() {
    const [searched, setSearched] = useState(false);
    const [hoveringOver, setHoveringOver] = useState(-1);
    const [locateRestaurant, setLocateRestaurant] = useState<(index: number) => void>(() => (_: number) => {
    });
    const [restaurantsData, setRestaurantsData] = useState<Restaurant[]>([]);

    const search = (query: string) => {
        fetchRestaurants(query).then((restaurants) => {
            console.log('Fetched restaurants:', restaurants);
            setRestaurantsData(restaurants);
        }).catch((error) => {
            console.error('Error fetching restaurants:', error);
        });
    }

    return (
        <StyleSheetManager shouldForwardProp={(prop) => !['$searched'].includes(prop)}>
            <PageContainer>
                <ContentContainer>
                    <MapComponent searched={searched} restaurants={restaurantsData} hoveringOver={hoveringOver}
                                  setLocateRestaurant={setLocateRestaurant}/>
                    <List searched={searched} restaurants={restaurantsData} setHoveringOver={setHoveringOver}
                          locateRestaurant={locateRestaurant}/>
                </ContentContainer>
                <Searchbar onSearch={search} setSearched={setSearched} searched={searched}/>
            </PageContainer>
        </StyleSheetManager>
    );
}
