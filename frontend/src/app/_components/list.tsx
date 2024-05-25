import {Box} from "@/app/_components/box";
import React from 'react';
import {Paper, Text, Button, Rating, Tooltip} from '@mantine/core';
import {IconClock} from '@tabler/icons-react';
import {styled} from "styled-components";

const Separator = styled.div`
    width: 100%;
    height: 1px;
    background-color: #00000045;
    margin-top: 20px;
    margin-bottom: 8px;
`;

interface Restaurant {
    name: string;
    rating: number;
    distance: string;
    closingTime: string;
}

interface ListProps {
    searched: boolean;
    restaurants: Restaurant[];
    setHoveringOver: (hoveringOver: number) => void;
}

const calculateTimeLeft = (closingTime: string) => {
    const now = new Date();
    const [closingHours, closingMinutes] = closingTime.split(':').map(Number);
    const closingDate = new Date();
    closingDate.setHours(closingHours, closingMinutes);
    const diffMs = closingDate.getTime() - now.getTime();
    if (diffMs <= 0) {
        return 'Closed';
    }
    const diffSecs = Math.round(diffMs / 1000);
    const hours = Math.floor(diffSecs / 3600);
    const minutes = Math.floor((diffSecs - hours * 3600) / 60);
    return `${hours > 0 ? hours + 'h ' : ''}${minutes > 0 ? String(minutes) + 'm ' : ''} until closing`;
};

const calculateAllTimeLeft = (restaurants: Restaurant[]) => {
    return restaurants.map(restaurant => calculateTimeLeft(restaurant.closingTime));
}

export const List = (props: ListProps) => {
    const [timeLeft, setTimeLeft] = React.useState(() => calculateAllTimeLeft(props.restaurants));

    React.useEffect(() => {
        const interval = setInterval(() => {
            setTimeLeft(calculateAllTimeLeft(props.restaurants));
        }, 10000);
        return () => clearInterval(interval);
    }, [props.restaurants]);

    return (
        <Box searched={props.searched}>
            {props.restaurants.map((restaurant, index) => (
                <div key={index}
                     style={{display: 'flex', flexDirection: 'column', marginBottom: '10px'}}
                     onMouseEnter={() => props.setHoveringOver(index)}>
                    <Paper style={{display: 'flex', justifyContent: 'space-between'}}>
                        <div style={{display: 'flex', flexDirection: 'column'}}>
                            <div style={{display: 'flex', alignItems: 'center'}}>
                                <Text size="xl">{restaurant.name}</Text>
                                <Rating value={restaurant.rating} fractions={10} readOnly style={{marginLeft: '28px'}}/>
                            </div>
                            <div style={{display: 'flex', alignItems: 'center'}}>
                                <Text size="md">Closes at {restaurant.closingTime}</Text>
                                <Tooltip label={timeLeft[index]} withArrow color={"blue"}
                                         transitionProps={{transition: 'pop', duration: 300}}>
                                    <IconClock style={{marginLeft: "4px", marginRight: "8px"}}/>
                                </Tooltip>
                                <Button style={{marginLeft: '10px', marginRight: '10px'}}>Menu</Button>
                            </div>
                        </div>
                        <Text size="xxl" style={{
                            textAlign: 'right',
                            fontSize: '30px',
                            fontWeight: 'bold'
                        }}>{restaurant.distance}</Text>
                    </Paper>
                    <Separator/>
                </div>
            ))}
        </Box>
    );
};