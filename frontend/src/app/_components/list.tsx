import {Box} from "@/app/_components/box";
import React from 'react';
import {Paper, Text, Button} from '@mantine/core';

interface Restaurant {
  name: string;
  rating: number;
  distance: string;
}

interface ListProps {
  searched: boolean;
  restaurants: Restaurant[];
}

export const List = (props: ListProps) => {
  return (
    <Box searched={props.searched}>
      {props.restaurants.map((restaurant, index) => (
        <Paper style={{marginBottom: '10px'}} key={index}>
          <Text size="xl">{restaurant.name}</Text>
          <Text size="sm">Rating: {restaurant.rating}</Text>
          <Text size="sm">Distance: {restaurant.distance}</Text>
          <Button>Menu</Button>
        </Paper>
      ))}
    </Box>
  );
};