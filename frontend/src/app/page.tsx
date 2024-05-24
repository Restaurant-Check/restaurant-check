'use client'

import {Searchbar} from "@/app/_components/searchbar";
import {Map} from "@/app/_components/map";
import {styled} from "styled-components";
import React, {useState} from "react";

const PageContainer = styled.main`
    height: 100vh;
    width: 100vw;
`;

export default function Home() {
    const [searched, setSearched] = useState(false);

    return (
        <PageContainer>
            <Searchbar onSearch={(query) => {
            }} setSearched={setSearched} searched={searched}/>
            <Map searched={searched} markers={[]}/>
        </PageContainer>
    );
}
