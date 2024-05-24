'use client'

import React, {useState} from 'react';
import {ActionIcon, rem, TextInput, useMantineTheme} from '@mantine/core';
import {IconArrowRight, IconSearch} from '@tabler/icons-react';
import {styled} from "styled-components";

const exampleSearches = [  // TODO: animate placeholder text to cycle through these
    'cheap Asian restaurant in Munich',
    'best pizza in Berlin',
    'vegan food in Hamburg',
    'sushi near me',
    'breakfast place in Frankfurt',
];

interface FormProps {
    searched: boolean;
}

const Form = styled.form<FormProps>`
    display: flex;
    justify-content: center;
    height: 100%;
    width: 100%;
    transition: align-items 0.3s ease-in-out;
`;

const StyledTextInput = styled(TextInput)<FormProps>`
    width: ${({searched}) => searched ? '40%' : '60%'};
    transition: all 0.3s ease-in-out;
    padding-top: ${({searched}) => searched ? "32px" : "25%"};
`;

interface SearchbarProps {
    onSearch: (query: string) => void;
    searched: boolean;
    setSearched: (searched: boolean) => void;
}

export const Searchbar = (props: SearchbarProps) => {
    const theme = useMantineTheme();
    const [query, setQuery] = useState('');

    const handleSearch = (event: React.FormEvent) => {
        event.preventDefault();
        if (query.trim() === '') return;
        props.setSearched(true);
        props.onSearch(query);
    };

    return (
        <Form onSubmit={handleSearch} searched={props.searched}>
            <StyledTextInput
                searched={props.searched}
                radius="xl"
                size="md"
                placeholder="Search for a restaurant..."
                rightSectionWidth={42}
                leftSection={<IconSearch style={{width: rem(18), height: rem(18)}} stroke={1.5}/>}
                rightSection={
                    <ActionIcon size={32} radius="xl" color={theme.primaryColor} variant="filled" type="submit">
                        <IconArrowRight style={{width: rem(18), height: rem(18)}} stroke={1.5}/>
                    </ActionIcon>
                }
                value={query}
                onChange={(event) => setQuery(event.currentTarget.value)}
            />
        </Form>
    );
};