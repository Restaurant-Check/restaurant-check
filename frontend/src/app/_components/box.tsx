import {styled} from "styled-components";
import React from "react";


const BoxWrapper = styled.div<{ $searched: boolean }>`
    padding: 20px;
    margin: 20px;
    border-radius: var(--mantine-radius-xl);
    box-shadow: 0 6px 32px rgba(0, 0, 0, 0.32);
    width: 75%;
    max-width: 1500px;
    transition: all 0.2s ease-in-out;
    opacity: ${props => props.$searched ? 1 : 0};
`;

interface BoxProps {
    $searched: boolean;
    children: React.ReactNode;
    style?: React.CSSProperties;
    id?: string;
}

export const Box = (props: BoxProps) => {
    return (
        <BoxWrapper $searched={props.$searched} style={props.style} id={props.id}>
            {props.children}
        </BoxWrapper>
    );
}