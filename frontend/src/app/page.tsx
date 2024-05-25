'use client'

import {Searchbar} from "@/app/_components/searchbar";
import {List} from "@/app/_components/list";
import {styled, StyleSheetManager} from "styled-components";
import React, {useState} from "react";
import {SampleData} from "@/app/_sample_data";
import dynamic from "next/dynamic";

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
    flex-direction: column;;
`;

export interface Restaurant {
    name: string;
    rating: number;
    distance: string;
    closingTime: string;
    top3MenuItems: string[];
    coordinates: [number, number];
}

export default function Home() {
    const [searched, setSearched] = useState(false);
    const [hoveringOver, setHoveringOver] = useState(-1);

    return ( // TODO: when scrolling, the map should stick to the top of the page and get a bit slimmer, also highlight the marker of the restaurant that is currently being hovered over
        <StyleSheetManager shouldForwardProp={(prop) => !['$searched'].includes(prop)}>
            <PageContainer>
                <ContentContainer>
                    <MapComponent searched={searched} restaurants={SampleData} hoveringOver={hoveringOver}/>
                    <List searched={searched} restaurants={SampleData} setHoveringOver={setHoveringOver}/>
                </ContentContainer>
                <Searchbar onSearch={(query) => {
                }} setSearched={setSearched} searched={searched}/>
            </PageContainer>
        </StyleSheetManager>
    );
}
