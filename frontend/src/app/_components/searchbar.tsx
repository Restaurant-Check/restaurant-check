'use client'

import React, {useEffect, useState} from 'react';
import {ActionIcon, rem, TextInput, useMantineTheme} from '@mantine/core';
import {IconArrowRight, IconSearch} from '@tabler/icons-react';
import {styled} from "styled-components";
import {useSpring, animated} from 'react-spring';

const exampleSearches = [
  'cheap Asian restaurant in Munich',
  'best pizza in Berlin',
  'vegan food in Hamburg',
  'sushi near me',
  'breakfast place in Frankfurt',
  'fancy dinner in Cologne',
  'fast food in Düsseldorf',
  'Italian restaurant in Stuttgart',
  'Mexican food in Dortmund',
  'burger in Essen',
];

interface FormProps {
  searched: boolean;
}

const Form = styled.form<FormProps>`
    display: flex;
    justify-content: center;
`;

const StyledTextInput = styled(TextInput)<FormProps>`
    position: absolute;
    width: ${({searched}) => searched ? '40%' : '60%'};
    transition: all 0.3s ease-in-out;
    padding-top: ${({searched}) => searched ? "32px" : "50%"};
`;

interface SubmitButtonProps {
  size: number;
  radius: string;
  color: string;
  variant: string;
  type: string;
  children: React.ReactNode;
}

const SubmitButton = styled(ActionIcon)<SubmitButtonProps>`
    transition: all 0.1s ease-in-out;
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

  const [placeholder, setPlaceholder] = useState("Search for a restaurant...");
  const [exampleIndex, setExampleIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [buttonPulsing, setButtonPulsing] = useState(false);

  useEffect(() => {
    if (isFocused) {
      const typingSpeed = isDeleting ? 15 : Math.random() * (110 - 50) + 50;
      const timeout = setTimeout(() => {
        if (!isDeleting && charIndex === exampleSearches[exampleIndex].length) {
          setTimeout(() => setIsDeleting(true), 1000);
        } else if (isDeleting && charIndex === 0) {
          setIsDeleting(false);
          setExampleIndex((exampleIndex + 1) % exampleSearches.length);
        } else {
          setPlaceholder(exampleSearches[exampleIndex].substring(0, charIndex + (isDeleting ? -1 : 1)));
          setCharIndex(prevCharIndex => prevCharIndex + (isDeleting ? -1 : 1));
        }
      }, typingSpeed);
      return () => clearTimeout(timeout);
    } else {
      setPlaceholder("Search for a restaurant...");
    }
  }, [isFocused, isDeleting, charIndex, exampleIndex]);


  useEffect(() => {
    setButtonPulsing(false)
    if (query !== '' && !props.searched) {
      const timeout = setTimeout(() => {
        setButtonPulsing(true);
      }, 3000);
      return () => clearTimeout(timeout);
    }
  }, [query]);

  const pulse = useSpring({
    from: {transform: 'scale(1)'},
    to: {transform: 'scale(1.08)'},
    config: {duration: 500},
    reset: buttonPulsing,
    reverse: buttonPulsing,
    onRest: () => setButtonPulsing(!buttonPulsing),
  });


  return (
    <Form onSubmit={handleSearch} searched={props.searched}>
      <StyledTextInput
        searched={props.searched}
        radius="xl"
        size="md"
        placeholder={placeholder}
        rightSectionWidth={42}
        leftSection={<IconSearch style={{width: rem(18), height: rem(18)}} stroke={1.5}/>}
        rightSection={
          <animated.div style={pulse}>
            <SubmitButton size={32} radius="xl" color={query !== "" ? theme.primaryColor : "gray"} variant="filled"
                          type="submit">
              <IconArrowRight style={{width: rem(18), height: rem(18)}} stroke={1.5}/>
            </SubmitButton>
          </animated.div>
        }
        value={query}
        onChange={(event) => setQuery(event.currentTarget.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      />
    </Form>
  );
}