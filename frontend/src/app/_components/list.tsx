import {Box} from "@/app/_components/box";
import React from 'react';
import {Paper, Text, Button, Rating, Tooltip} from '@mantine/core';
import {IconClock, IconMap} from '@tabler/icons-react';
import {styled} from "styled-components";
import {Restaurant} from "@/app/page";

interface ListProps {
    searched: boolean;
    restaurants: Restaurant[];
    setHoveringOver: (hoveringOver: number) => void;
    locateRestaurant: (index: number) => void;
}

interface ButtonProps {
    onClick?: () => void;
    children: string;
    variant: string;
    radius: string;
}

const Separator = styled.div`
    width: 100%;
    height: 2px;
    background-color: #00000055;
    margin-top: 20px;
    margin-bottom: 8px;
`;

const Divider = styled.div`
    width: 2px;
    height: 100%;
    background-color: #00000055;
    margin-right: 20px;
    margin-left: 20px;
`;

const MenuButton = styled(Button)<ButtonProps>`
    margin-top: 10px;
`;

const MenuItemsTable = ({menuItems}: { menuItems: string[] }) => {
    const menuItemsProcessed = menuItems.reduce((acc: { [key: string]: { name: string, price: string }[] }, item) => {
        const [fullCategory, price] = item.split(' | ');
        const [category, name] = fullCategory.split(/:(.+)/);
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push({name: name.trim(), price});
        return acc;
    }, {});

    return (
        <table>
            <tbody>
            {Object.entries(menuItemsProcessed).map(([category, items]: [string, {
                name: string,
                price: string
            }[]], index) => (
                <React.Fragment key={index}>
                    {items.map(({name, price}, index) => (
                        <tr key={index}>
                            <td><Text>{index === 0 ? category : ''}</Text></td>
                            <td><Text>{name} </Text></td>
                            <td><Text style={{marginLeft: '4px'}}> {price} €</Text></td>
                        </tr>
                    ))}
                </React.Fragment>
            ))}
            <tr>
                <td>
                    <MenuButton variant="light" radius="lg">Show whole menu</MenuButton>
                </td>
            </tr>
            </tbody>
        </table>
    );
};

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
        <Box $searched={props.searched}>
            {props.restaurants.map((restaurant, index) => (
                <div key={index}
                     style={{display: 'flex', flexDirection: 'column', marginBottom: '10px'}}
                     onMouseEnter={() => props.setHoveringOver(index)}
                     onMouseLeave={() => props.setHoveringOver(-1)}
                >
                    <Paper style={{display: 'flex', justifyContent: 'space-between'}}>
                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <div style={{display: 'flex', flexDirection: 'column'}}>
                                <div style={{display: 'flex', alignItems: 'center'}}>
                                    <Text size="xl">{restaurant.name}</Text>
                                    <Rating value={restaurant.rating} fractions={10} readOnly
                                            style={{marginLeft: '28px'}}/>
                                </div>
                                <Paper style={{
                                    display: 'flex',
                                    alignItems: 'flex-end',
                                    flexDirection: 'column',
                                    justifyContent: 'space-between',
                                    height: '100%',
                                }}>
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                    }}>
                                        <Text size="md">Closes at {restaurant.closingTime}</Text>
                                        <Tooltip label={timeLeft[index]} withArrow color={"blue"}
                                                 transitionProps={{transition: 'pop', duration: 300}}>
                                            <IconClock style={{marginLeft: "4px", marginRight: "8px"}}/>
                                        </Tooltip>
                                    </div>
                                    <Button variant="light" size="xs" radius="lg"
                                            style={{marginTop: 'auto', marginBottom: '4px'}}
                                            onClick={() => props.locateRestaurant(index)}
                                    >
                                        <IconMap/>
                                    </Button>
                                </Paper>
                            </div>
                            <Divider/>
                            <MenuItemsTable menuItems={restaurant.top3MenuItems}/>
                        </div>
                        <Text size="xxl" style={{
                            textAlign: 'right',
                            fontSize: '30px',
                            fontWeight: 'bold'
                        }}>{restaurant.distance}</Text>
                    </Paper>
                    {index < props.restaurants.length - 1 && <Separator/>}
                </div>
            ))}
        </Box>
    );
};