'use client'

import {Searchbar} from "@/app/_components/searchbar";
import {MapComponent} from "@/app/_components/mapComponent";
import {List} from "@/app/_components/list";
import {styled} from "styled-components";
import React, {useState} from "react";

const PageContainer = styled.main`
    height: 100vh;
    width: 100vw;
`;

const ContentContainer = styled.div`
    position: absolute;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    flex-direction: column;
    top: 64px;
`;

export default function Home() {
  const [searched, setSearched] = useState(false);

  return (
    <PageContainer>
      <ContentContainer>
        <MapComponent searched={searched} markers={[]}/>
        <List searched={searched}/>
      </ContentContainer>
      <Searchbar onSearch={(query) => {
      }} setSearched={setSearched} searched={searched}/>
    </PageContainer>
  );
}
