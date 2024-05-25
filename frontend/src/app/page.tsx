'use client'

import {Searchbar} from "@/app/_components/searchbar";
import {MapComponent} from "@/app/_components/mapComponent";
import {List} from "@/app/_components/list";
import {styled} from "styled-components";
import React, {useState} from "react";

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
    flex-direction: column;;
`;

const SampleData = [ // TODO: Add coordinates to the data
    {
        name: 'Restaurant 1',
        rating: 4.5,
        distance: '1.2km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 2',
        rating: 4.2,
        distance: '2.1km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 3',
        rating: 4.8,
        distance: '0.5km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 4',
        rating: 4.1,
        distance: '3.2km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 5',
        rating: 4.9,
        distance: '0.3km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 6',
        rating: 4.6,
        distance: '2.5km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 7',
        rating: 4.3,
        distance: '1.7km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 8',
        rating: 4.7,
        distance: '0.8km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 9',
        rating: 4.4,
        distance: '2.9km',
        closingTime: '22:00',
    },
    {
        name: 'Restaurant 10',
        rating: 4.0,
        distance: '3.9km',
        closingTime: '22:00',
    },
];

export default function Home() {
    const [searched, setSearched] = useState(false);
    const [hoveringOver, setHoveringOver] = useState(-1);

    return ( // TODO: when scrolling, the map should stick to the top of the page and get a bit slimmer, also highlight the marker of the restaurant that is currently being hovered over
        <PageContainer>
            <ContentContainer>
                <MapComponent searched={searched} markers={[]}/>
                <List searched={searched} restaurants={SampleData} setHoveringOver={setHoveringOver}/>
            </ContentContainer>
            <Searchbar onSearch={(query) => {
            }} setSearched={setSearched} searched={searched}/>
        </PageContainer>
    );
}
