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

const SampleData = [
  {
    name: 'Restaurant 1',
    rating: 4.5,
    distance: '1.2km',
  },
  {
    name: 'Restaurant 2',
    rating: 4.2,
    distance: '2.1km',
  },
  {
    name: 'Restaurant 3',
    rating: 4.8,
    distance: '0.5km',
  },
  {
    name: 'Restaurant 4',
    rating: 4.1,
    distance: '3.2km',
  },
  {
    name: 'Restaurant 5',
    rating: 4.9,
    distance: '0.3km',
  },
  {
    name: 'Restaurant 6',
    rating: 4.6,
    distance: '2.5km',
  },
  {
    name: 'Restaurant 7',
    rating: 4.3,
    distance: '1.7km',
  },
  {
    name: 'Restaurant 8',
    rating: 4.7,
    distance: '0.8km',
  },
  {
    name: 'Restaurant 9',
    rating: 4.4,
    distance: '2.9km',
  },
  {
    name: 'Restaurant 10',
    rating: 4.0,
    distance: '3.9km',
  },
];

export default function Home() {
  const [searched, setSearched] = useState(false);

  return (
    <PageContainer>
      <ContentContainer>
        <MapComponent searched={searched} markers={[]}/>
        <List searched={searched} restaurants={SampleData}/>
      </ContentContainer>
      <Searchbar onSearch={(query) => {
      }} setSearched={setSearched} searched={searched}/>
    </PageContainer>
  );
}
